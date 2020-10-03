package com.example.mlthreatdetect.ui.home;

import android.app.Activity;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProviders;

import com.example.mlthreatdetect.R;

public class HomeFragment extends Fragment implements View.OnClickListener{

    private HomeViewModel homeViewModel;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        homeViewModel =
                ViewModelProviders.of(this).get(HomeViewModel.class);
        View root = inflater.inflate(R.layout.fragment_home, container, false);
        Button camButton = (Button) root.findViewById(R.id.recordButton);
        camButton.setOnClickListener(this);
        /**
         *         final TextView textView = root.findViewById(R.id.text_home);
         *         homeViewModel.getText().observe(getViewLifecycleOwner(), new Observer<String>() {
         *             @Override
         *             public void onChanged(@Nullable String s) {
         *                 textView.setText(s);
         *             }
         *         });
         */

        return root;
    }

    static final int REQUEST_VIDEO_CAPTURE = 1;

    @Override
    public void onClick(View v) {
        Intent takeVideoIntent = new Intent(MediaStore.ACTION_VIDEO_CAPTURE);
        // TODO: Figure out why this check isn't functioning like it should...
        // if (takeVideoIntent.resolveActivity(getParentFragment().getActivity().getPackageManager()) != null) {
            startActivityForResult(takeVideoIntent, REQUEST_VIDEO_CAPTURE);
        // }
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent intent) {
        if (requestCode == REQUEST_VIDEO_CAPTURE && resultCode == getActivity().RESULT_OK) {
            Uri videoUri = intent.getData();
        }
    }
}