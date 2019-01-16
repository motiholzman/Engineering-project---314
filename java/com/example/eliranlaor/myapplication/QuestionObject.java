package com.example.eliranlaor.myapplication;

import android.app.Activity;
import android.os.Parcel;
import android.os.Parcelable;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class QuestionObject extends Activity implements Parcelable {

    private static final String PK = "pk";
    private static final String ID = "id";
    private static final String QUESTION = "question";
    private static final String TOPIC = "topic";
    private static final String EXTENSIONS = "extensions";
    private static final String DIFFICULTY = "difficulty";
    private static final String HINT = "hint";
    private static final String GAME_MODE = "game_mode";
    private static final String OWNER = "owner";
    private static final String ANSWER = "answer";

    private static final String FIELDS = "fields";

    private int id;
    private String question;
    private String topic;
    private String extensions;
    private String difficulty;
    private String hint;
    private String gameMode;
    private String owner;
    private String answer;

    public QuestionObject(String q) {
        question = q;
        answer = "";
    }

    public QuestionObject() {
        id = 0;
        question = "";
        answer = "";
    }

    /**
     * copy c-tor from JSON object
     */
    public QuestionObject(JSONObject jsonObject) {
        try {
            id = Integer.parseInt(jsonObject.getString(PK));
            question = jsonObject.getJSONObject(FIELDS).getString(QUESTION);
            topic = jsonObject.getJSONObject(FIELDS).getString(TOPIC);
            extensions = jsonObject.getJSONObject(FIELDS).getString(EXTENSIONS);
            difficulty = jsonObject.getJSONObject(FIELDS).getString(DIFFICULTY);
            hint = jsonObject.getJSONObject(FIELDS).getString(HINT);
            gameMode = jsonObject.getJSONObject(FIELDS).getString(GAME_MODE);
            owner = jsonObject.getJSONObject(FIELDS).getString(OWNER);
            answer = "";
        }
        catch (JSONException ex) {
            ex.printStackTrace();
        }

    }

    public String getQuestion() {
        return question;
    }

    public String getAnswer() {
        return answer;
    }

    public void setId(int i) {
        id = i;
    }

    public void setQuestion(String q1) {
        question = q1;
    }

    public void setAnswer(String ans) {
        answer = ans;
    }

    public String getTopic() {
        return topic;
    }

    public int getId() {
        return id;
    }

    public String getOwner() {
        return owner;
    }

    public String getHint() {
        return hint;
    }

    public String getGameMode() {
        return gameMode;
    }

    public String getExtensions() {
        return extensions;
    }

    public String getDifficulty() {
        return difficulty;
    }


    static Map<String,String> convertQuestionToMap(QuestionObject q) {
        Map<String, String> converted = new HashMap<>();
        converted.put(ID , String.valueOf(q.id));
        converted.put(TOPIC, q.topic);
        converted.put(EXTENSIONS, q.extensions);
        converted.put(DIFFICULTY, q.difficulty);
        converted.put(HINT, q.hint);
        converted.put(GAME_MODE, q.gameMode);
        converted.put(OWNER, q.owner);
        converted.put(ANSWER, q.answer);
        return converted;
    }

    // Parcelling part
    public QuestionObject(Parcel in){
        String[] data = new String[9];

        in.readStringArray(data);
        // the order needs to be the same as in writeToParcel() method
        this.id =Integer.parseInt(data[0]);
        this.question = data[1];
        this.topic = data[2];
        this.extensions = data[3];
        this.difficulty = data[4];
        this.hint = data[5];
        this.gameMode = data[6];
        this.owner = data[7];
        this.answer = data[8];
    }

    public int describeContents(){
        return 0;
    }

    public void writeToParcel(Parcel dest, int flags) {
        dest.writeStringArray(new String[] {String.valueOf(this.id), this.question, this.topic,
                this.extensions, this.difficulty, this.hint, this.gameMode, this.owner,
                this.answer});
    }

    public static final Parcelable.Creator CREATOR = new Parcelable.Creator() {
        public QuestionObject createFromParcel(Parcel in) {
            return new QuestionObject(in);
        }

        public QuestionObject[] newArray(int size) {
            return new QuestionObject[size];
        }
    };
}
