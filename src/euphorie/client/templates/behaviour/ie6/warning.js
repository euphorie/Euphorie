
var msg1 = "Warning";
var msg2 = "";
var msg_html = "<br clear=all><p><b>English</b>: This web application is not compatible with the version of the webbrowser you are using. Some features may not work as designed. To improve your experience please upgrade to a newer version or use an alternative browser, such as Crome, Firefox or Safari.</p>" +
"<p><b>Български</b>: Уеб приложението не е съвместимо с версията на уеб браузъра, която използвате. Възможно е някои функции да не работят, както се очаква. За да подобрите изпълнението, обновете версията на браузъра или използвайте друг браузър, например Google Chrome, Mozilla Firefox или Safari.</p>" +
"<p><b>Català</b>: Aquesta aplicació web no és compatible amb la versió del navegador web que s'està utilitzant. Algunes característiques poden no funcionar segons el previst. Si us plau, actualitzeu el navegador amb una nova versió o utilitzi un navegador alternatiu, com Crome, Firefox o Safari.</p>"+
"<p><b>Čeština</b>: Tato webová aplikace není kompatibilní s verzí prohlížeče, kterou používáte. Některé prvky nemusí fungovat tak, jak byly navrženy. Za účelem zajištění optimální funkčnosti prosím upgradujte na novější verzi nebo použijte jiný prohlížeč, například Chrome, Firefox nebo Safari.</p>"+
"<p><b>Dansk</b>: Denne webapplikation er ikke kompatibel med den webbrowserversion, du anvender. Visse elementer funger måske ikke efter hensigten. For bedre at kunne udnytte anvendelsesmulighederne bør du opgradere til en nyere version eller anvende en anden browser, for eksempel Crome, Firefox eller Safari.</p>"+
"<p><b>Deutsch</b>: Diese Web-Anwendung ist mit der von Ihnen verwendeten Webbrowser-Version nicht kompatibel. Manche Funktionen funktionieren möglicherweise nicht wie vorgesehen. Um Ihre Nutzungsmöglichkeiten zu verbessern, empfehlen wir, zu einer neueren Version zu wechseln oder einen anderen Browser (z. B. Chrome, Firefox oder Safari) zu verwenden.</p>"+
"<p><b>Ελληνικά</b>: Αυτή η διαδικτυακή εφαρμογή δεν είναι συμβατή με την έκδοση του περιηγητή που χρησιμοποιείτε. Ορισμένες εφαρμογές ενδέχεται να μην λειτουργούν όπως είχαν σχεδιαστεί. Για καλύτερη απόδοση, αναβαθμίστε τον περιηγητή σας στην πιο πρόσφατη έκδοση ή χρησιμοποιήστε κάποιον εναλλακτικό περιηγητή όπως Crome, Firefox ή Safari.</p>"+
"<p><b>Español</b>: Esta aplicación para la Web no es compatible con la versión del navegador que está utilizando. Algunas características pueden no funcionar según lo previsto. Para mejorar su uso de la aplicación, le aconsejamos instalar una nueva versión o utilizar un navegador alternativo, como Crome, Firefox o Safari.</p>"+
"<p><b>Eesti</b>: See veebirakendus ei ühildu veebibrauseriga. Mõned funktsioonid ei pruugi täielikult toimida. Paremaks kasutamiseks uuenda versiooni või vali alternatiivne brauser, nt Chrome, Firefox või Safari.</p>"+
"<p><b>Suomi</b>: Tämä verkkosovellus ei ole yhteensopiva käyttämäsi verkkoselaimen version kanssa. Jotkin ominaisuudet eivät ehkä toimi kuten on suunniteltu. Parantaaksesi toimintaa päivitä selain uudempaan versioon tai käytä jotakin muuta selainta, esimerkiksi Cromea, Firefoxia tai Safaria.</p>"+
"<p><b>Français</b>: Cette application web n’est pas compatible avec la version actuelle de votre navigateur web. Il se peut que certaines fonctionnalités ne fonctionnent pas comme prévu. Pour votre confort, veuillez télécharger une version plus récente ou utiliser un autre navigateur, comme Chrome, Firefox ou Safari.</p>"+
"<p><b>Magyar</b>: Ez a webes alkalmazás nem kompatibilis az Ön által használt webböngésző verziójával. Előfordulhat, hogy egyes funkciók nem a tervezettnek megfelelően működnek. Annak érdekében, hogy az eszközt a legoptimálisabb módon tudja használni, váltson az újabb verzióra vagy másik böngészőre, mint például a Chrome, a Firefox vagy a Safari.</p>"+
"<p><b>Íslenska</b>: Þessi vefhugbúnaður er ekki samhæfður við vafraútgáfuna sem þú notar. Ekki er víst að allir eiginleikar virki eins og ætlast er til. Til þess að upplifun þín verði betri skaltu uppfæra í nýrri útgáfu eða nota annan vafra, svo sem Crome, Firefox eða Safari.</p>"+
"<p><b>Italiano</b>: Quest’applicazione web non è compatibile con la versione del browser che si sta usando. Alcune funzionalità potrebbero non funzionare come dovrebbero. Per migliorare la propria esperienza, si prega di aggiornare a una versione più recente o di usare un browser alternativo come Crome, Firefox o Safari.</p>"+
"<p><b>Lietuviskai</b>: Ši interneto programa neveikia naudojant jūsų interneto naršyklės versiją. Kai kurios funkcijos gali neveikti. Kad programa veiktų geriau, atnaujinkite savo naršyklės versiją arba naudokitės kita naršykle, pvz., Chrome, Firefox arba Safari.</p>"+
"<p><b>Latviešu</b>: Šī tīmekļa lietojumprogramma nav saderīga ar tīmekļa pārlūkprogrammas versiju, kuru Jūs izmantojat. Dažas funkcijas var nedarboties, kā paredzēts. Lai uzlabotu iespējas, lūdzam veikt jauninājumu uz jaunāku versiju vai izmantot citu pārlūkprogrammu, piemēram, Crome, Firefox vai Safari.</p>"+
"<p><b>Malti</b>: Din l-applikazzjoni web mhix kumpatibbli mal-verżjoni tal-brawżer li qed tuża.. Xi funzjonijiet jistgħu ma jaħdmux kif suppost. Biex ittejjeb l-esperjenza tiegħek, jekk jogħġbok aġġorna għal verżjoni iżjed riċenti jew uża brawżer differenti bħal Crome, Firefox jew Safari.</p>"+
"<p><b>Nederlands</b>: Deze webtoepassing is niet verenigbaar met de versie van de webbrowser die u gebruikt. Enkele functies werken wellicht niet als werd voorzien. Voer een upgrade uit naar een nieuwere versie of gebruik een andere browser, zoals Chrome, Firefox of Safari, om de mogelijkheden beter te kunnen benutten.</p>"+
"<p><b>Norsk</b>: Denne nettapplikasjonen er ikke kompatibel med den nettleserversjonen du bruker. Det kan hende at enkelte funksjoner ikke virker som de skal. For å forbedre opplevelsen bør du oppgradere til en nyere versjon eller bruke en annen nettleser, for eksempel Chrome, Firefox eller Safari.</p>"+
"<p><b>Polski</b>: Niniejsza aplikacja internetowa nie jest kompatybilna z wersją stosowanej przeglądarki internetowej. Niektóre elementy mogą nie funkcjonować w zaplanowany sposób. Aby móc w pełni korzystać z dostępnych funkcji, należy zainstalować nowszą wersję programu lub inną przeglądarkę, tj. Chrome, Firefox czy Safari.</p>"+
"<p><b>Português</b>: Esta aplicação Web não é compatível com a versão do seu navegador de Internet. Algumas funções poderão não funcionar corretamente. Para melhorar a sua experiência, atualize o seu navegador para uma versão mais recente ou utilize outro navegador, como o Chrome, o Firefox ou o Safari.</p>"+
"<p><b>Română</b>: Această aplicaţie web nu este compatibilă cu versiunea browserului web pe care-l folosiţi. Unele caracteristici s-ar putea să nu funcţioneze la parametrii prevăzuţi. Pentru o mai bună utilizare a aplicaţiei, vă rugăm să actualizaţi versiunea sau să folosiţi alt browser, de exemplu Chrome, Firefox sau Safari.</p>"+
"<p><b>Slovenčina</b>: Táto webová aplikácia nie je kompatibilná s verziou prehliadača, ktorú používate. Môže sa stať, že niektoré funkcie nebudú fungovať tak, ako majú. Za účelom zaistenia optimálnej funkčnosti, inštalujte si najnovšiu verziu alebo použite iný prehliadač, ako napr. Chrome, Firefox alebo Safari.</p>"+
"<p><b>Slovenščina</b>: Ta spletna aplikacija ni združljiva z različico spletnega brskalnika, ki jo uporabljate. Nekatere njene funkcije zato morda ne bodo delovale, kot so bile zasnovane. Za boljši ogled si naložite novejšo različico brskalnika ali pa uporabite drug brskalnik, kot je denimo Chrome, Firefox ali Safari.</p>"+
"<p><b>Svenska</b>: Denna webbapplikation är inte kompatibel med den webbläsare du använder. Vissa funktioner fungerar kanske inte som tänkt. Uppgradera till en nyare version eller använd en annan webbläsare, t.ex. Crome, Firefox eller Safari, för att förbättra upplevelsen.</p>"+
"";
var _lang_bg = document.createElement('span');

_lang_bg.innerHTML = msg_html;
var msg3 = "";
var br1 = "Internet Explorer 9+";
var br2 = "Firefox";
var br3 = "Safari";
var br4 = "Opera";
var br5 = "Chrome";
var url1 = "http://www.microsoft.com/windows/Internet-explorer/default.aspx";
var url2 = "http://www.mozilla.com/firefox/";
var url3 = "http://www.apple.com/safari/download/";
var url4 = "http://www.opera.com/download/";
var url5 = "http://www.google.com/chrome";
var imgPath;


function e(str) {imgPath = str;
var _body = document.getElementsByTagName('body')[0];
var _d = document.createElement('div');
var _l = document.createElement('div');
var _h = document.createElement('h1');
var _p1 = document.createElement('p');
var _p2 = document.createElement('p');
var _x = document.createElement('a');
var _top_close = document.createElement('button');
var _bot_close = document.createElement('button');
var _ul = document.createElement('ul');
var _li1 = document.createElement('li');
var _li2 = document.createElement('li');
var _li3 = document.createElement('li');
var _li4 = document.createElement('li');
var _li5 = document.createElement('li');
var _ico1 = document.createElement('div');
var _ico2 = document.createElement('div');
var _ico3 = document.createElement('div');
var _ico4 = document.createElement('div');
var _ico5 = document.createElement('div');
var _lit1 = document.createElement('div');
var _lit2 = document.createElement('div');
var _lit3 = document.createElement('div');
var _lit4 = document.createElement('div');
var _lit5 = document.createElement('div');
var _br1 = document.createElement('br');
var _br2 = document.createElement('br');
_body.appendChild(_l);
_body.appendChild(_d);
/*_d.appendChild(_h);
_d.appendChild(_p1);
_d.appendChild(_p2);*/
_d.appendChild(_top_close);
_top_close.setAttribute('id','_tc');
_d.appendChild(_ul);
_ul.appendChild(_li1);
_ul.appendChild(_li2);
_ul.appendChild(_li3);
_ul.appendChild(_li4);
_ul.appendChild(_li5);
_li1.appendChild(_ico1);
_li2.appendChild(_ico2);
_li3.appendChild(_ico3);
_li4.appendChild(_ico4);
_li5.appendChild(_ico5);
_li1.appendChild(_lit1);
_li2.appendChild(_lit2);
_li3.appendChild(_lit3);
_li4.appendChild(_lit4);
_li5.appendChild(_lit5);
_d.appendChild(_lang_bg);
_d.appendChild(_bot_close);
_bot_close.setAttribute('id','_bc');
_d.setAttribute('id','_d');
_l.setAttribute('id','_l');
_x.setAttribute('id','_x');
_h.setAttribute('id','_h');
_p1.setAttribute('id','_p1');
_p2.setAttribute('id','_p2');
_ul.setAttribute('id','_ul');
_li1.setAttribute('id','_li1');
_li2.setAttribute('id','_li2');
_li3.setAttribute('id','_li3');
_li4.setAttribute('id','_li4');
_li5.setAttribute('id','_li5');
_ico1.setAttribute('id','_ico1');
_ico2.setAttribute('id','_ico2');
_ico3.setAttribute('id','_ico3');
_ico4.setAttribute('id','_ico4');
_ico5.setAttribute('id','_ico5');
_lit1.setAttribute('id','_lit1');
_lit2.setAttribute('id','_lit2');
_lit3.setAttribute('id','_lit3');
_lit4.setAttribute('id','_lit4');
_lit5.setAttribute('id','_lit5');
var _width = document.documentElement.clientWidth;
var _height = document.documentElement.clientHeight;
var _dl = document.getElementById('_l');
_dl.style.width =  _width+"px";
_dl.style.height = _height+"px";
_dl.style.position = "absolute";
_dl.style.top = "0px";
_dl.style.left = "0px";
_dl.style.filter = "alpha(opacity=50)";
var _dd = document.getElementById('_d');
_ddw = 660;
_ddh = 500;
_dd.style.width = _ddw+"px";
/*_dd.style.height = _ddh+"px";*/
_dd.style.position = "absolute";
_dd.style.top = ((_height-_ddh)/2)+"px";
_dd.style.left = ((_width-_ddw)/2)+"px";
_dd.style.padding = "20px";
_dd.style.background = "#fff";
_dd.style.border = "1px solid #ccc";
_dd.style.fontFamily = "'Lucida Grande','Lucida Sans Unicode',Arial,Verdana,sans-serif";
_dd.style.listStyleType = "none";
_dd.style.color = "#4F4F4F";
_dd.style.fontSize = "10px";
_dd.style.zIndex = '99';

var _tc = document.getElementById('_tc');
var _bc = document.getElementById('_bc');
_tc.appendChild(document.createTextNode('close'));
_tc.style.marginRight = 'auto';
_tc.style.marginLeft = 'auto';
_tc.style.marginBottom = '1em';

_bc.appendChild(document.createTextNode('close'));
_bc.style.marginRight = 'auto';
_bc.style.marginLeft = 'auto';
_bc.style.marginBottom = '1em';

var close = function () {
    _body.removeChild(_d);
    _body.removeChild(_l);
};
_tc.onclick = close;
_bc.onclick = close;

/*_h.appendChild(document.createTextNode(msg1));*/
/*var _hd = document.getElementById('_h');
_hd.style.display = "block";
_hd.style.fontSize = "1em";
_hd.style.marginBottom = "0.5em";
_hd.style.color = "#333";
_hd.style.fontFamily = "Helvetica,Arial,sans-serif";
_hd.style.fontWeight = "bold";*/
/*_p1.appendChild(document.createTextNode(msg2));
var _p1d = document.getElementById('_p1');
_p1d.style.marginBottom = "1em";*/
/*_p2.appendChild(document.createTextNode(msg3));*/
/*_p2.appendChild(_lang_bg);*/
/*var _p2d = document.getElementById('_p2');
_p2d.style.marginBottom = "1em";*/
var _uld = document.getElementById('_ul');
_uld.style.listStyleImage = "none";
_uld.style.listStylePosition = "outside";
_uld.style.listStyleType = "none";
_uld.style.margin = "0 px auto";
_uld.style.padding = "0px";
_uld.style.paddingLeft = "0px";
_uld.style.marginLeft = "0px";
var _li1d = document.getElementById('_li1');
var _li2d = document.getElementById('_li2');
var _li3d = document.getElementById('_li3');
var _li4d = document.getElementById('_li4');
var _li5d = document.getElementById('_li5');
var _li1ds = _li1d.style;
var _li2ds = _li2d.style;
var _li3ds = _li3d.style;
var _li4ds = _li4d.style;
var _li5ds = _li5d.style;
_li1ds.background = _li2ds.background = _li3ds.background = _li4ds.background = _li5ds.background = "transparent url('"+imgPath+"background_browser.gif') no-repeat scroll left top";
_li1ds.cursor = _li2ds.cursor = _li3ds.cursor = _li4ds.cursor = _li5ds.cursor = "pointer";
_li1d.onclick = function() {window.location = url1;};
 _li2d.onclick = function() {window.location = url2;};
 _li3d.onclick = function() {window.location = url3;};
 _li4d.onclick = function() {window.location = url4;};
 _li5d.onclick = function() {window.location = url5;};
 _li1ds.styleFloat = _li2ds.styleFloat = _li3ds.styleFloat = _li4ds.styleFloat = _li5ds.styleFloat = "left";
_li1ds.width = _li2ds.width = _li3ds.width = _li4ds.width = _li5ds.width = "120px";
_li1ds.height = _li2ds.height = _li3ds.height = _li4ds.height = _li5ds.height = "122px";
_li1ds.margin = _li2ds.margin = _li3ds.margin = _li4ds.margin = _li5ds.margin = "0 10px 10px 0";
_li1ds.display = _li2ds.display = _li3ds.display = _li4ds.display = _li5ds.display = "inline-block";
var _ico1d = document.getElementById('_ico1');
var _ico2d = document.getElementById('_ico2');
var _ico3d = document.getElementById('_ico3');
var _ico4d = document.getElementById('_ico4');
var _ico5d = document.getElementById('_ico5');
var _ico1ds = _ico1d.style;
var _ico2ds = _ico2d.style;
var _ico3ds = _ico3d.style;
var _ico4ds = _ico4d.style;
var _ico5ds = _ico5d.style;
_ico1ds.cursor = _ico2ds.cursor = _ico3ds.cursor = _ico4ds.cursor = _ico5ds.cursor = "pointer";
_ico1ds.width = _ico2ds.width = _ico3ds.width = _ico4ds.width = _ico5ds.width = "100px";
_ico1ds.height = _ico2ds.height = _ico3ds.height = _ico4ds.height = _ico5ds.height = "100px";
_ico1ds.margin = _ico2ds.margin = _ico3ds.margin = _ico4ds.margin = _ico5ds.margin = "1px auto";
_ico1ds.background = "transparent url('"+imgPath+"browser_ie.gif') no-repeat scroll left top";
_ico2ds.background = "transparent url('"+imgPath+"browser_firefox.gif') no-repeat scroll left top";
_ico3ds.background = "transparent url('"+imgPath+"browser_safari.gif') no-repeat scroll left top";
_ico4ds.background = "transparent url('"+imgPath+"browser_opera.gif') no-repeat scroll left top";
_ico5ds.background = "transparent url('"+imgPath+"browser_chrome.gif') no-repeat scroll left top";
_lit1.appendChild(document.createTextNode(br1));
_lit2.appendChild(document.createTextNode(br2));
_lit3.appendChild(document.createTextNode(br3));
_lit4.appendChild(document.createTextNode(br4));
_lit5.appendChild(document.createTextNode(br5));
var _lit1d = document.getElementById('_lit1');
var _lit2d = document.getElementById('_lit2');
var _lit3d = document.getElementById('_lit3');
var _lit4d = document.getElementById('_lit4');
var _lit5d = document.getElementById('_lit5');
var _lit1ds = _lit1d.style;
var _lit2ds = _lit2d.style;
var _lit3ds = _lit3d.style;
var _lit4ds = _lit4d.style;
var _lit5ds = _lit5d.style;
_lit1ds.color = _lit2ds.color = _lit3ds.color = _lit4ds.color = _lit5ds.color = "#808080";
_lit1ds.fontSize = _lit2ds.fontSize = _lit3ds.fontSize = _lit4ds.fontSize = _lit5ds.fontSize = "0.8em";
_lit1ds.height = _lit2ds.height = _lit3ds.height = _lit4ds.height = _lit5ds.height = "18px";
_lit1ds.lineHeight = _lit2ds.lineHeight = _lit3ds.lineHeight = _lit4ds.lineHeight = _lit5ds.lineHeight = "17px";
_lit1ds.margin = _lit2ds.margin = _lit3ds.margin = _lit4ds.margin = _lit5ds.margin = "1px auto";
_lit1ds.width = _lit2ds.width = _lit3ds.width = _lit4ds.width = _lit5ds.width = "118px";
_lit1ds.textAlign = _lit2ds.textAlign = _lit3ds.textAlign = _lit4ds.textAlign = _lit5ds.textAlign = "center";
_lit1ds.cursor = _lit2ds.cursor = _lit3ds.cursor = _lit4ds.cursor = _lit5ds.cursor = "pointer";
}
