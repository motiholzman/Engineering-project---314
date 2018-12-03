package com.example.eliranlaor.myapplication;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import java.util.ArrayList;

public class HomeScreen extends AppCompatActivity {


    ArrayList<EditText> jokesArray = new ArrayList<>();
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        /*Bindibg XML to class*/
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        /*Bindibg XML to class - done*/

        /*switching to contribute screen*/
        Button contributeBtn = (Button) findViewById(R.id.ctbBtn);
        contributeBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(HomeScreen.this, ContributeMain.class);
                startActivity(intent);
                finish();
            }
        });
        /*switching to contribute screen - Done*/

        /*switching to review screen*/
        Button reviewBtn = (Button) findViewById(R.id.revBtn);
        reviewBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(HomeScreen.this, ReviewMain.class);
                startActivity(intent);
                finish();
            }
        });
        /*switching to review screen - done*/


    }
}
