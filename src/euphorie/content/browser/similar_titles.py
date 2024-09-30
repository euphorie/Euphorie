from collections import defaultdict
from euphorie.content import MessageFactory as _
from euphorie.content.surveygroup import ISurveyGroup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from plone import api
from plone.autoform.form import AutoExtensibleForm
from plone.memoize import ram
from plone.memoize.view import memoize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from z3c.form import button
from z3c.form import form
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.interface import Interface


def _forever_cache_key(method, *args, **kwargs):
    return method.__name__


class ISimilarTitleSchema(Interface):
    min_similarity = schema.Float(
        title=_("Minimum similarity"),
        description=_("Minimum similarity between titles"),
        default=0.5,
        required=True,
        min=0.0,
        max=1.0,
    )

    max_similarity = schema.Float(
        title=_("Maximum similarity"),
        description=_("Maximum similarity between titles"),
        default=1.0,
        required=True,
        min=0.0,
        max=1.0,
    )


class SimilarTitles(AutoExtensibleForm, form.Form):
    """
    A form that allows you to find and display risks with similar titles.
    """

    schema = ISimilarTitleSchema
    ignoreContext = True
    form_name = _("Similar Titles OiRA Tool")
    show_form = True

    label = _("Similar Titles OiRA Tool")
    description = _("This tool allows you to find objects with similar titles.")

    @property
    def template(self):
        return self.index

    def redirect(self, target=None, message=None, message_type="info"):
        if target is None:
            target = self.context.absolute_url()
        if message is not None:
            api.portal.show_message(
                message=message, request=self.request, type=message_type
            )
        self.request.response.redirect(target)

    @property
    @memoize
    def extracted_data(self):
        """extract_data returns data and errors from the form.
        We want just the data
        """
        return self.extractData()[0]

    @property
    def min_similarity(self):
        return self.extracted_data.get("min_similarity", 0.5)

    @property
    def max_similarity(self):
        return self.extracted_data.get("max_similarity", 1.0)

    @property
    @memoize
    def tool_cache(self):
        return {}

    def get_tool_for_brain(self, brain):
        cache_key = "/".join(brain.getPath().split("/")[:6])
        cache = self.tool_cache
        value = cache.get(cache_key)
        if value is not None:
            return value
        obj = brain.getObject()
        for obj in obj.aq_chain:
            if ISurveyGroup.providedBy(obj):
                value = obj
                cache[cache_key] = value
                return value

    @ram.cache(_forever_cache_key)
    def initialize_nltk(self):
        """Initialize the NLTK library"""
        import nltk

        nltk.download("punkt")
        nltk.download("stopwords")
        nltk.download("wordnet")

    @property
    @ram.cache(_forever_cache_key)
    def published_surveys_paths(self):
        """Return a list of published survey paths"""
        brains = api.content.find(portal_type="euphorie.surveygroup")
        paths = []
        for brain in brains:
            obj = brain.getObject()
            published = getattr(obj, "published", "")
            if published:
                paths.append(f"{brain.getPath()}/{published}")
        return paths

    @property
    @memoize
    def similar_brains(self):
        self.initialize_nltk()
        brains = api.content.find(
            portal_type="euphorie.risk",
            sort_on="sortable_title",
            path=self.published_surveys_paths,
        )

        def preprocess_text(line):
            # Tokenize the text into individual words
            tokens = word_tokenize(line.lower())

            # Remove stop words
            stop_words = set(stopwords.words("german"))
            filtered_tokens = [word for word in tokens if word not in stop_words]

            # Lemmatize the words
            lemmatizer = WordNetLemmatizer()
            lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

            # Join the tokens back into a single string
            preprocessed_text = " ".join(lemmatized_tokens)

            return preprocessed_text

        lines = [brain.Title for brain in brains]
        preprocessed_lines = [preprocess_text(line) for line in lines]
        # Calculate TF-IDF vectors https://en.wikipedia.org/wiki/Tf%E2%80%93idf
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(preprocessed_lines)

        # Calculate cosine similarity between all pairs of lines
        similarity_matrix = cosine_similarity(tfidf_matrix)

        # Group the lines that have a similarity score between
        # self.min_similarity and self.max_similarity
        similar_brains = defaultdict(list)
        min_similarity = self.min_similarity
        max_similarity = self.max_similarity
        for idx_x, brain_x in enumerate(brains):
            for idx_y, brain_y in enumerate(brains):
                # skip pairs on the diagonal, they have obviously a similarity of 1
                if idx_x != idx_y:
                    similarity = similarity_matrix[idx_x, idx_y]
                    if min_similarity <= similarity <= max_similarity:
                        similar_brains[brain_x].append((brain_y, round(similarity, 2)))
        return similar_brains

    @button.buttonAndHandler(_("Search"))
    def handle_search(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.results_html = api.content.get_view(
            context=self.context, request=self.request, name="similar-titles-results"
        )()

    @button.buttonAndHandler(_("Show stored result"))
    def handle_show_stored_result(self, action):
        self.redirect(target=f"{self.context.absolute_url()}/@@similar-titles-stored")

    @button.buttonAndHandler(_("Cancel"), name="cancel")
    def handle_cancel(self, action):
        self.redirect(message=_("Operation cancelled."))


class SimilarTitlesResults(SimilarTitles):
    @button.buttonAndHandler(_("Search"))
    def handle_search(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return


class SimilarTitlesStored(SimilarTitles):
    show_form = False

    @property
    def results_html(self):
        annotations = IAnnotations(api.portal.get())
        return annotations.get("euphorie.content.similar_titles_html", "")

    @results_html.setter
    def results_html(self, value):
        annotations = IAnnotations(api.portal.get())
        annotations["euphorie.content.similar_titles_html"] = value
