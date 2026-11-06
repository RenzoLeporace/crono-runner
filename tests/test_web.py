"""Browser build: page adaptation, staging and the bridge shared with Android."""
import importlib.util
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('build_web',ROOT/'tools'/'build_web.py')
build_web=importlib.util.module_from_spec(spec);spec.loader.exec_module(build_web)

TEMPLATE=f'''<html lang="en-us"><script src="{build_web.CDN}pythons.js" type=module id="site" data-os="vtx,snd,gui">
    platform.document.body.style.background = "#7f7f7f"
    print("Ready to start ! Please click/touch page")
--></script><head><meta name="viewport" content="width=device-width"><title>CRONO</title>
<script src="{build_web.CDN}browserfs.min.js"></script>
</head><body><p>Loading, please wait</p></body></html>'''


class WebBuildTests(unittest.TestCase):
    def test_page_uses_the_local_runtime_and_the_bridge(self):
        html=build_web.customize(TEMPLATE)
        self.assertNotIn('pygame-web.github.io',html)
        self.assertIn('src="./runtime/pythons.js"',html)
        self.assertNotIn('browserfs',html)
        self.assertIn('<html lang="es">',html)
        self.assertIn('data-os="snd,gui"',html)
        self.assertIn('<script src="crono-web.js"></script>',html)
        self.assertLess(html.index('crono-web.js'),html.index('</head>'))
        self.assertEqual(len(re.findall(r'<meta name="viewport"',html)),1)
        self.assertIn('<title>CRONO · Ecos del tiempo</title>',html)
        self.assertIn('id="crono-rotate"',html)
        self.assertNotIn('#7f7f7f',html)
        self.assertNotIn('Ready to start',html)

    def test_staging_copies_the_game_with_the_browser_entry_point(self):
        original=build_web.APP
        with tempfile.TemporaryDirectory() as temp:
            build_web.APP=Path(temp)/'webapp'
            try:
                build_web.stage()
                self.assertEqual((build_web.APP/'main.py').read_text(encoding='utf-8'),(ROOT/'web'/'main.py').read_text(encoding='utf-8'))
                self.assertTrue((build_web.APP/'crono'/'game.py').is_file())
                self.assertTrue((build_web.APP/'assets'/'audio').is_dir())
                self.assertTrue((build_web.APP/'COPYRIGHT.txt').is_file())
                self.assertFalse(list(build_web.APP.rglob('__pycache__')))
                self.assertFalse((build_web.APP/'saves').exists(),'no se publican guardados locales')
                self.assertFalse((build_web.APP/'contenido').exists(),'no se publican bancos docentes locales')
            finally:
                build_web.APP=original

    def test_browser_entry_point_waits_for_saves_and_keeps_the_game_loop(self):
        source=(ROOT/'web'/'main.py').read_text(encoding='utf-8')
        compile(source,'web/main.py','exec')
        self.assertLess(source.index('CronoWeb.isReady()'),source.index('initialize()'))
        for call in ('game.events()','game.update(','game.render()','await asyncio.sleep(','game.save.write()'):
            self.assertIn(call,source)

    def test_web_bridge_offers_every_android_bridge_method(self):
        java=(ROOT/'android'/'app'/'src'/'main'/'java'/'org'/'renzoleporace'/'crono'/'MainActivity.java').read_text(encoding='utf-8')
        android=set(re.findall(r'@JavascriptInterface public \w+ (\w+)\(',java))
        script=(ROOT/'web'/'crono-web.js').read_text(encoding='utf-8')
        bridge=script[script.index('const puente = {'):script.index('window.CronoAndroid = puente')]
        web=set(re.findall(r'^    (\w+)\(',bridge,re.M))
        self.assertTrue(android,'no se encontraron métodos del puente de Android')
        self.assertEqual(android-web,set(),'métodos de Android sin equivalente web')

    @unittest.skipUnless(shutil.which('node'),'Node.js no está instalado')
    def test_web_bridge_behaviour(self):
        result=subprocess.run(['node','--test',str(ROOT/'web'/'crono-web.test.mjs')],capture_output=True,text=True,encoding='utf-8',timeout=120)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)


if __name__=='__main__':
    unittest.main()
