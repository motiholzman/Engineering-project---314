package com.example.eliranlaor.myapplication;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.util.Map;

public class ContributeMainGame extends AppCompatActivity {

    static final private String ADD_ANSWER_TO_DB_URL = "/app_server/AddAnswerToDB";
    private HttpPostTask task;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_contribute_main_game);


        /*binding vars*/
        final String topic = "Hello!";
        final EditText et = (EditText) findViewById(R.id.editText_answer);
        TextView questionView = (TextView) findViewById(R.id.questionText);
        Button back = (Button) findViewById(R.id.retBtn);
        Button doneSimplying = (Button) findViewById(R.id.simplifyDone);
        /*binding vars - done*/

        final QuestionObject curQuestion = getIntent().getExtras().getParcelable("questionToUser");
        questionView.setText(curQuestion.getQuestion());




        back.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                /*TODO - should ask user if he really wants to click 'back' because he already lost poits getting here, also change target activity to topics main*/
                Intent intent = new Intent(ContributeMainGame.this, ContributeMain.class);
                startActivity(intent);
                finish();
            }
        });

        doneSimplying.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String answer = et.getText().toString();
                curQuestion.setAnswer(answer);
                Map<String, String> postData = QuestionObject.convertQuestionToMap(curQuestion);
                task  = new HttpPostTask(postData,ContributeMainGame.this);
                task.execute(HttpPostTask.BASE_URL+ ADD_ANSWER_TO_DB_URL);
            }
        });
    }

    public void onBackPressed(){
        Intent intent = new Intent(ContributeMainGame.this, HomeScreen.class);
        startActivity(intent);
        finish();
    }




}
