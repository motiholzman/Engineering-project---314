package com.example.eliranlaor.myapplication;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class contributeTopTrending extends AppCompatActivity {

    Button anotherRound, backToTopics;
    TextView topTrending;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_contribute_top_trending);
        anotherRound = (Button) findViewById(R.id.retBtn2);
        backToTopics = (Button) findViewById(R.id.retToTopics);
        topTrending = (TextView)  findViewById(R.id.textView_topTrending);
        final String topic = getIntent().getExtras().getString("topic");

        anotherRound.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                /*TODO - should ask user if he really wants to click 'back' because he already lost poits getting here*/
                Intent intent = new Intent(contributeTopTrending.this, ContributeMainGame.class);
                intent.putExtra("topic", topic);
                startActivity(intent);
                finish();
            }
        });

        backToTopics.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                /*TODO - change the target actvity to topics main*/
                Intent intent = new Intent(contributeTopTrending.this, ContributeMain.class);
                startActivity(intent);
                finish();
            }
        });
    }

    public void onBackPressed(){
        Intent intent = new Intent(contributeTopTrending.this, HomeScreen.class);
        startActivity(intent);
        finish();
    }
}
