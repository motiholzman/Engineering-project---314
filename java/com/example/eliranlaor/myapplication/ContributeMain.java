package com.example.eliranlaor.myapplication;

import android.content.Intent;
import android.graphics.Typeface;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class ContributeMain extends AppCompatActivity {


    private Typeface tf1;
    private TextView title;
    private HttpGetTask task;
    static final private String TITLE_FONT_NAME = "gasalt_black.ttf";
    static final private String QUESTION_BY_TOPIC_URL = "/app_server/getQuestionByTopic";
    static final private String SPORT_URL = "/Sport";
    static final private String GENERAL_URL = "/General";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.contribute_main);
        //getWindow().getDecorView().setBackgroundColor(Color.BLUE);

        /* defining a font to the Title */
        title = (TextView) findViewById(R.id.categoryTitle);
        tf1 = Typeface.createFromAsset(getAssets() , ContributeMain.TITLE_FONT_NAME);
        title.setTypeface(tf1);

        /* defining a font to the Title  - done*/

        /*set back button to home screen*/
        Button retBtn = (Button) findViewById(R.id.retBut);
        retBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(ContributeMain.this, HomeScreen.class);
                startActivity(intent);
                finish();
            }
        });
        /*set back button to home screen - done*/


        /*set catA button to home screen*/
        Button catA = (Button) findViewById(R.id.catA);

        catA.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                task = new HttpGetTask(ContributeMain.this);
                task.execute(HttpPostTask.BASE_URL + QUESTION_BY_TOPIC_URL + SPORT_URL);
            }
        });
        /*set catA button to home screen - done*/


        /*set catB button to home screen*/
        Button catB = (Button) findViewById(R.id.catB);

        catB.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                task = new HttpGetTask(ContributeMain.this);
                task.execute(HttpPostTask.BASE_URL + QUESTION_BY_TOPIC_URL+ GENERAL_URL);
            }
        });
        /*set catB button to home screen - done*/
    }
}
