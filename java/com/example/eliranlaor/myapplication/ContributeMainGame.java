package com.example.eliranlaor.myapplication;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class ContributeMainGame extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_contribute_main_game);


        /*binding vars*/
        final EditText et = (EditText) findViewById(R.id.editText_answer);
        TextView questionView = (TextView) findViewById(R.id.questionText);
        Button back = (Button) findViewById(R.id.retBtn);
        Button doneSimplying = (Button) findViewById(R.id.simplifyDone);
        /*binding vars - done*/


        final String topic = getIntent().getExtras().getString("topic");
        /*TODO - here we need to get the question from the server*/
        questionView.setText(topic); //TODO this should be the question, not topic!!

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
                /*TODO - add answer to server*/
                Intent intent = new Intent(ContributeMainGame.this, contributeTopTrending.class);
                intent.putExtra("topic", topic);
                startActivity(intent);
            }
        });

    }

    public void onBackPressed(){
        Intent intent = new Intent(ContributeMainGame.this, HomeScreen.class);
        startActivity(intent);
        finish();
    }


}
