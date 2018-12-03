package com.example.eliranlaor.myapplication;

import android.content.Intent;
import android.graphics.Typeface;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class ContributeMain extends AppCompatActivity {


    Typeface tf1;
    TextView title;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.contribute_main);
        //getWindow().getDecorView().setBackgroundColor(Color.BLUE);

        /* defining a font to the Title */
        title = (TextView) findViewById(R.id.categoryTitle);
        tf1 = Typeface.createFromAsset(getAssets() , "gasalt_black.ttf");
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
                Intent intent = new Intent(ContributeMain.this, ContributeMainGame.class);
                intent.putExtra("topic", "Sports");
                startActivity(intent);
            }
        });
        /*et catA button to home screen - done*/
    }
}
