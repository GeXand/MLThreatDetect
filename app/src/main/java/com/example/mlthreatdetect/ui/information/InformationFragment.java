package com.example.mlthreatdetect.ui.information;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProviders;

import com.example.mlthreatdetect.R;

public class InformationFragment extends Fragment {

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {

        View root = inflater.inflate(R.layout.fragment_information, container, false);
        final TextView textView1 = root.findViewById(R.id.text_information1);
        final TextView textView2 = root.findViewById(R.id.text_information2);
        final TextView textView3 = root.findViewById(R.id.text_information3);
        final TextView textView4 = root.findViewById(R.id.text_information4);

        // TODO: pull data using location to determine locally available resources
        textView1.setText("Emergency resources (NYC): ");
        textView2.setText("Mental Health: \n 1 (888) 692-9355");
        textView3.setText("Domestic Violence: \n 1 (800) 621-4673");
        textView4.setText("Conflict De-escalation: \n (123) 456-7890");

        return root;
    }
}