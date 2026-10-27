package org.renzoleporace.crono;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.KeyEvent;
import android.view.View;
import android.view.WindowManager;
import android.webkit.JavascriptInterface;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.EditText;
import android.widget.Toast;
import android.speech.tts.TextToSpeech;
import android.speech.tts.Voice;
import org.json.JSONObject;
import org.json.JSONArray;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.concurrent.*;

/** The same Python game, with all runtime assets packaged for offline play. */
public final class MainActivity extends Activity {
    private WebView web;
    private final ExecutorService network = Executors.newFixedThreadPool(2);
    private final ConcurrentHashMap<String,String> jobs = new ConcurrentHashMap<>();
    private static final String HOST = "appassets.androidplatform.net";
    private static final int SAVE_LIMIT=32*1024*1024;
    private String pendingFileJob;
    private String pendingExport;
    private TextToSpeech speech;
    private boolean speechReady;
    private String pendingSpeech;

    private void say(String value) {
        pendingSpeech=value;
        if(speech==null){
            speech=new TextToSpeech(this,status->web.post(()->{
                if(isFinishing()||isDestroyed())return;
                Voice selected=null;
                if(status==TextToSpeech.SUCCESS&&speech!=null&&speech.getVoices()!=null){
                    for(Voice voice:speech.getVoices()){
                        if(!"es".equals(voice.getLocale().getLanguage())||voice.isNetworkConnectionRequired()||voice.getFeatures()!=null&&voice.getFeatures().contains("notInstalled"))continue;
                        selected=voice;if("AR".equals(voice.getLocale().getCountry()))break;
                    }
                }
                if(selected!=null){speech.setVoice(selected);speechReady=true;speech.speak(pendingSpeech,TextToSpeech.QUEUE_FLUSH,null,"crono-help");}
                else Toast.makeText(this,"No hay voz española instalada. Puedes seguir las señales de la pantalla.",Toast.LENGTH_LONG).show();
            }));
        }else if(speechReady)speech.speak(value,TextToSpeech.QUEUE_FLUSH,null,"crono-help");
        else Toast.makeText(this,"La voz aún no está disponible.",Toast.LENGTH_SHORT).show();
    }

    @Override public void onCreate(Bundle saved) {
        super.onCreate(saved);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_FULLSCREEN|View.SYSTEM_UI_FLAG_HIDE_NAVIGATION|View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY);
        web = new WebView(this);setContentView(web);
        web.setBackgroundColor(0xff0d1b25);
        web.getSettings().setJavaScriptEnabled(true);
        web.getSettings().setDomStorageEnabled(true);
        web.getSettings().setDefaultTextEncodingName("UTF-8");
        web.getSettings().setSupportZoom(false);
        web.getSettings().setAllowFileAccess(false);
        web.getSettings().setAllowContentAccess(false);
        web.getSettings().setMediaPlaybackRequiresUserGesture(false);
        web.addJavascriptInterface(new Bridge(), "CronoAndroid");
        web.setWebChromeClient(new WebChromeClient(){
            @Override public boolean onConsoleMessage(android.webkit.ConsoleMessage message){
                android.util.Log.d("CRONO",message.message());return true;
            }
        });
        web.setWebViewClient(new WebViewClient() {
            @Override public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                Uri uri=request.getUrl();
                if (!HOST.equals(uri.getHost())) return response(403,"text/plain",new ByteArrayInputStream(new byte[0]));
                String path=uri.getPath();if(path==null||path.equals("/"))path="/index.html";
                if(path.contains(".."))return response(403,"text/plain",new ByteArrayInputStream(new byte[0]));
                try{return response(200,mime(path),getAssets().open(path.substring(1)));}
                catch(IOException error){return response(404,"text/plain",new ByteArrayInputStream(new byte[0]));}
            }
            @Override public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                if(HOST.equals(request.getUrl().getHost()))return false;
                if(request.hasGesture()&&"https".equals(request.getUrl().getScheme()))openExternal(request.getUrl().toString());
                return true;
            }
        });
        web.loadUrl("https://"+HOST+"/index.html");
    }

    private WebResourceResponse response(int status,String mime,InputStream body) {
        Map<String,String> headers=new HashMap<>();headers.put("Cache-Control","no-cache");headers.put("Access-Control-Allow-Origin","https://"+HOST);
        return new WebResourceResponse(mime,"UTF-8",status,status==200?"OK":"Unavailable",headers,body);
    }
    private String mime(String path) {
        if(path.endsWith(".js"))return "application/javascript";
        if(path.endsWith(".wasm"))return "application/wasm";
        if(path.endsWith(".html"))return "text/html";
        if(path.endsWith(".json"))return "application/json";
        if(path.endsWith(".py"))return "text/x-python";
        if(path.endsWith(".png"))return "image/png";
        if(path.endsWith(".ogg"))return "audio/ogg";
        return "application/octet-stream";
    }
    private void openExternal(String url) {
        runOnUiThread(()->{try{startActivity(new Intent(Intent.ACTION_VIEW,Uri.parse(url)));}catch(Exception ignored){}});
    }
    private File safeFile(String relative) throws IOException {
        if(relative==null||!(relative.startsWith("saves/")||relative.startsWith("contenido/")))throw new IOException("Ruta inválida");
        File root=new File(getFilesDir(),"crono");File target=new File(root,relative);
        if(!target.getCanonicalPath().startsWith(root.getCanonicalPath()+File.separator))throw new IOException("Ruta inválida");
        return target;
    }
    private static String readText(InputStream stream,int limit) throws IOException {
        ByteArrayOutputStream out=new ByteArrayOutputStream();byte[] buffer=new byte[8192];int n;
        while((n=stream.read(buffer))>=0){if(out.size()+n>limit)throw new IOException("Archivo demasiado grande");out.write(buffer,0,n);}
        return new String(out.toByteArray(),StandardCharsets.UTF_8);
    }
    private static String encoded(String text){return android.util.Base64.encodeToString(text.getBytes(StandardCharsets.UTF_8),android.util.Base64.NO_WRAP);}
    private static String decoded(String text){return new String(android.util.Base64.decode(text,android.util.Base64.DEFAULT),StandardCharsets.UTF_8);}
    private static String asciiJson(String text){
        StringBuilder out=new StringBuilder();
        for(int i=0;i<text.length();i++){char c=text.charAt(i);if(c>127)out.append(String.format(Locale.ROOT,"\\u%04x",(int)c));else out.append(c);}
        return out.toString();
    }
    private JSONObject post(String address,String route,JSONObject body) throws Exception {
        URL url=new URL(address+route);
        if(!"http".equals(url.getProtocol()))throw new IOException("Usa la IP de la sala local.");
        HttpURLConnection connection=(HttpURLConnection)url.openConnection();
        connection.setConnectTimeout(3500);connection.setReadTimeout(4500);connection.setInstanceFollowRedirects(false);
        connection.setRequestProperty("Connection","close");
        connection.setRequestMethod("POST");connection.setDoOutput(true);connection.setRequestProperty("Content-Type","application/json; charset=utf-8");
        byte[] payload=body.toString().getBytes(StandardCharsets.UTF_8);
        connection.setFixedLengthStreamingMode(payload.length);
        try{
            try(OutputStream output=connection.getOutputStream()){output.write(payload);}
            int code=connection.getResponseCode();InputStream source=code>=400?connection.getErrorStream():connection.getInputStream();
            if(source==null)throw new IOException("La sala no respondió.");
            JSONObject response;
            try(InputStream input=source){response=new JSONObject(readText(input,8_000_000));}
            android.util.Log.d("CRONO","Sala "+route+" HTTP "+code);
            if(code!=200)throw new IOException(response.optString("error","No se pudo conectar."));
            return response;
        }finally{connection.disconnect();}
    }

    public final class Bridge {
        @JavascriptInterface public boolean performanceLogging(){return getIntent().getBooleanExtra("crono_performance",false);}
        @JavascriptInterface public boolean speak(String contents){
            try{
                String value=decoded(contents);
                if(value.length()>3500)return false;
                runOnUiThread(()->say(value));return true;
            }catch(Exception error){return false;}
        }
        @JavascriptInterface public String loadFiles() {
            JSONObject result=new JSONObject();
            for(String path:new String[]{"saves/perfiles.json","saves/docente.json"}){
                String contents=loadFile(path);
                if(contents!=null)try{result.put(path,decoded(contents));}catch(Exception ignored){}
            }
            return asciiJson(result.toString());
        }
        @JavascriptInterface public String loadFile(String path) {
            try(InputStream input=new FileInputStream(safeFile(path))){return encoded(readText(input,SAVE_LIMIT));}
            catch(Exception error){return null;}
        }
        @JavascriptInterface public boolean saveFile(String path,String contents) {
            try{
                byte[] bytes=decoded(contents).getBytes(StandardCharsets.UTF_8);
                if(bytes.length>SAVE_LIMIT)return false;File target=safeFile(path);target.getParentFile().mkdirs();
                File temp=new File(target.getPath()+".tmp");
                try(FileOutputStream output=new FileOutputStream(temp)){output.write(bytes);output.getFD().sync();}
                return temp.renameTo(target);
            }catch(Exception error){return false;}
        }
        @JavascriptInterface public boolean deleteFile(String path) {try{return safeFile(path).delete();}catch(Exception error){return false;}}
        @JavascriptInterface public void openUrl(String encodedUrl) {try{String url=decoded(encodedUrl);if(url.startsWith("https://"))openExternal(url);}catch(Exception ignored){}}
        @JavascriptInterface public void finishGame() {runOnUiThread(()->finish());}
        @JavascriptInterface public String enqueue(String encoded) {
            String id=UUID.randomUUID().toString();jobs.put(id,"{\"ready\":false}");
            network.execute(()->{
                JSONObject answer=new JSONObject();
                try{
                    JSONObject task=new JSONObject(encoded);String address=task.getString("address");String token=task.optString("token","");
                    JSONObject activity;String operation=task.getString("operation");
                    if(operation.equals("join")){
                        JSONObject profile=task.getJSONObject("profile");JSONObject body=new JSONObject(profile.toString());
                        body.put("code",task.getString("code"));body.put("token",token);activity=post(address,"/join",body);token=activity.getString("token");
                    }else{
                        JSONObject body=new JSONObject();body.put("token",token);body.put("records",task.getJSONObject("records"));body.put("practice",task.optBoolean("practice",false));post(address,"/results",body);
                        activity=post(address,"/activity",new JSONObject().put("token",token));
                    }
                    JSONObject ranking=post(address,"/rankings",new JSONObject().put("token",token));
                    answer.put("result",new JSONObject().put("token",token).put("activity",activity).put("rankings",ranking));
                }catch(Exception error){android.util.Log.w("CRONO","No se pudo actualizar la sala",error);try{answer.put("error",error.getMessage()==null?"Sin conexión":error.getMessage());}catch(Exception ignored){}}
                try{answer.put("ready",true);}catch(Exception ignored){}jobs.put(id,answer.toString());
            });return id;
        }
        @JavascriptInterface public String poll(String id) {
            String result=jobs.get(id);if(result==null)return "{\"ready\":true,\"error\":\"Solicitud desconocida\"}";
            if(result.contains("\"ready\":true"))jobs.remove(id);return asciiJson(result);
        }
        @JavascriptInterface public String editText(String initial,int limit,boolean multiline,boolean password) {
            String id=UUID.randomUUID().toString();jobs.put(id,"{\"ready\":false}");
            runOnUiThread(()->{
                EditText input=new EditText(MainActivity.this);input.setText(decoded(initial));input.setSelectAllOnFocus(true);
                input.setSingleLine(!multiline);input.setInputType(password?129:multiline?131073:1);
                input.setFilters(new android.text.InputFilter[]{new android.text.InputFilter.LengthFilter(Math.max(1,Math.min(1000,limit)))});
                AlertDialog dialog=new AlertDialog.Builder(MainActivity.this).setTitle("CRONO · Escribir").setView(input)
                    .setPositiveButton("Aceptar",(buttonDialog,which)->{
                        try{jobs.put(id,new JSONObject().put("ready",true).put("text",input.getText().toString()).toString());}catch(Exception ignored){}
                    }).setNegativeButton("Cancelar",(ignored,which)->jobs.put(id,"{\"ready\":true}"))
                    .setOnCancelListener(ignored->jobs.put(id,"{\"ready\":true}")).create();
                dialog.show();input.requestFocus();dialog.getWindow().setSoftInputMode(android.view.WindowManager.LayoutParams.SOFT_INPUT_STATE_ALWAYS_VISIBLE);
            });return id;
        }
        @JavascriptInterface public String pickQuestionBank(){
            String id=UUID.randomUUID().toString();jobs.put(id,"{\"ready\":false}");
            runOnUiThread(()->{
                pendingFileJob=id;pendingExport=null;
                Intent intent=new Intent(Intent.ACTION_OPEN_DOCUMENT);intent.setType("application/json");intent.addCategory(Intent.CATEGORY_OPENABLE);
                startActivityForResult(intent,1001);
            });return id;
        }
        @JavascriptInterface public String exportDocument(String name,String contents,String mime){
            String id=UUID.randomUUID().toString();jobs.put(id,"{\"ready\":false}");
            runOnUiThread(()->{
                pendingFileJob=id;pendingExport=decoded(contents);
                Intent intent=new Intent(Intent.ACTION_CREATE_DOCUMENT);intent.setType(mime);intent.addCategory(Intent.CATEGORY_OPENABLE);intent.putExtra(Intent.EXTRA_TITLE,name);
                startActivityForResult(intent,1002);
            });return id;
        }
    }
    @Override protected void onActivityResult(int request,int result,Intent data){
        super.onActivityResult(request,result,data);
        if(request!=1001&&request!=1002)return;
        String id=pendingFileJob;String contents=pendingExport;pendingFileJob=null;pendingExport=null;
        if(id==null)return;
        if(result!=RESULT_OK||data==null||data.getData()==null){jobs.put(id,"{\"ready\":true}");return;}
        Uri uri=data.getData();
        network.execute(()->{
            JSONObject answer=new JSONObject();
            try{
                if(request==1001){try(InputStream input=getContentResolver().openInputStream(uri)){answer.put("text",readText(input,4_000_000));}}
                else{try(OutputStream output=getContentResolver().openOutputStream(uri)){output.write(contents.getBytes(StandardCharsets.UTF_8));}answer.put("saved",true);}
            }catch(Exception error){try{answer.put("error",error.getMessage());}catch(Exception ignored){}}
            try{answer.put("ready",true);}catch(Exception ignored){}jobs.put(id,answer.toString());
        });
    }
    @Override public void onBackPressed() {
        web.dispatchKeyEvent(new KeyEvent(KeyEvent.ACTION_DOWN,KeyEvent.KEYCODE_ESCAPE));web.dispatchKeyEvent(new KeyEvent(KeyEvent.ACTION_UP,KeyEvent.KEYCODE_ESCAPE));
    }
    @Override public void onWindowFocusChanged(boolean focused){
        super.onWindowFocusChanged(focused);
        if(focused)getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_FULLSCREEN|View.SYSTEM_UI_FLAG_HIDE_NAVIGATION|View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY);
    }
    @Override protected void onDestroy(){network.shutdownNow();if(speech!=null)speech.shutdown();if(web!=null){web.removeJavascriptInterface("CronoAndroid");web.destroy();}super.onDestroy();}
    @Override protected void onPause(){if(speech!=null)speech.stop();if(web!=null)web.evaluateJavascript("window.dispatchEvent(new Event('blur'))",null);super.onPause();}
}
