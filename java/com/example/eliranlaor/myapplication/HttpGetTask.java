package com.example.eliranlaor.myapplication;

import android.app.Activity;
import android.content.Intent;
import android.os.AsyncTask;

import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class HttpGetTask extends AsyncTask<String, Void, Void>{
    private Activity activity;
    // This is the JSON body of the post
    private JSONObject questionData;

    QuestionObject newQuestionToUser;


    /**
     * c-tor
     * @param activity: the activity which we came from.
     */
    public HttpGetTask(Activity activity) {
        this.activity = activity;
    }

    /**
     * this method creates the GET request.
     * @param params: this array of strings contains the additional data for the request (such as URL)
     */
    @Override
    protected Void doInBackground(String... params) {

        try {
            URL url = new URL(params[0]);

            // Create the urlConnection
            HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
            urlConnection.setDoInput(true);
            urlConnection.setRequestMethod("GET");

            int statusCode = urlConnection.getResponseCode();

            if (statusCode ==  200) {

                InputStream inputStream = new BufferedInputStream(urlConnection.getInputStream());

                String response = HttpPostTask.convertInputStreamToString(inputStream);
                response = response.substring(1,response.length()-1);
                questionData = new JSONObject(response);

            } else {
                System.err.println("http response was not valid");
            }

        } catch (Exception e) {
            //TODO - handle this exception
            e.printStackTrace();
        }
        return null;
    }

    @Override
    protected void onPostExecute(Void v) {

        newQuestionToUser = new QuestionObject(questionData);
        Intent intent = new Intent(activity, ContributeMainGame.class);
        intent.putExtra("questionToUser", newQuestionToUser);
        activity.startActivity(intent);
    }





}