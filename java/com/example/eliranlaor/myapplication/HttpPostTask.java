package com.example.eliranlaor.myapplication;

import android.app.Activity;
import android.content.Intent;
import android.os.AsyncTask;

import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Map;

public class HttpPostTask extends AsyncTask<String, Void, Void>{
    private Activity activity;
    // This is the JSON body of the post
    JSONObject postData;
    JSONObject questionData;

    QuestionObject newQuestionToUser;

    //http://127.0.0.1:7000
    static final String BASE_URL = "http://10.0.2.2:7000";

    // This is a constructor that allows you to pass in the JSON body
    public HttpPostTask(Map<String, String> postData, Activity activity) {
        this.activity = activity;
        if (postData != null) {
            this.postData = new JSONObject(postData);
        }
    }

    // This is a function that we are overriding from AsyncTask. It takes Strings as parameters because that is what we defined for the parameters of our async task
    @Override
    protected Void doInBackground(String... params) {

        try {
            // This is getting the url from the string we passed in
            URL url = new URL(params[0]);

            // Create the urlConnection
            HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
            urlConnection.setDoInput(true);
            urlConnection.setDoOutput(true);
            urlConnection.setRequestProperty("Content-Type", "application/json");
            urlConnection.setRequestMethod("POST");

            // Send the post body
            if (this.postData != null) {
                OutputStreamWriter writer = new OutputStreamWriter(urlConnection.getOutputStream());
                writer.write(postData.toString());
                writer.flush();
            }

            int statusCode = urlConnection.getResponseCode();

            if (statusCode ==  200) {

                InputStream inputStream = new BufferedInputStream(urlConnection.getInputStream());

                String response = HttpPostTask.convertInputStreamToString(inputStream);
                response = response.substring(1,response.length()-1);
                questionData = new JSONObject(response);

            } else {
                System.err.println("http response was not valid");
                // Status code is not 200
                // Do something to handle the error
            }

        } catch (Exception e) {
            //TODO - handle this exception
            e.printStackTrace();
        }
        return null;
    }

    @Override
    protected void onPostExecute(Void v) {

        //FIXME WHERE SHOULD WE GO FROM HERE
        newQuestionToUser = new QuestionObject(questionData);
        Intent intent = new Intent(activity, ContributeMainGame.class);
        intent.putExtra("questionToUser", newQuestionToUser);
        activity.startActivity(intent);
    }


    static String convertInputStreamToString(InputStream is) {
        String line = "";
        StringBuilder total = new StringBuilder();
        BufferedReader rd = new BufferedReader(new InputStreamReader(is));
        try {
            while ((line = rd.readLine()) != null) {
                total.append(line);
            }
        } catch (Exception e) {
            //TODO - handle this exception
            e.printStackTrace();
        }
        return total.toString();
    }



}