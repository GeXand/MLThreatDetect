package com.example.mlthreatdetect.ui.home;

import android.Manifest;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.core.app.ActivityCompat;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProviders;

import com.example.mlthreatdetect.MainActivity;
import com.example.mlthreatdetect.R;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.ml.common.modeldownload.FirebaseModelDownloadConditions;
import com.google.firebase.ml.common.modeldownload.FirebaseModelManager;
import com.google.firebase.ml.custom.FirebaseCustomRemoteModel;

import org.tensorflow.lite.Interpreter;

import java.io.File;

public class HomeFragment extends Fragment {

    private ProgressBar confidenceLevel;
    private TextView modelResultInfo;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {

        View root = inflater.inflate(R.layout.fragment_home, container, false);

        confidenceLevel = (ProgressBar) root.findViewById(R.id.progressBar);
        modelResultInfo = (TextView) root.findViewById(R.id.modelInfo);
        modelResultInfo.setText("Awaiting video to analyze");

        Button camButton = (Button) root.findViewById(R.id.recordButton);
        camButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent takeVideoIntent = new Intent(MediaStore.ACTION_VIDEO_CAPTURE);
                // TODO: Figure out why this check isn't functioning like it should...
                // if (takeVideoIntent.resolveActivity(getParentFragment().getActivity().getPackageManager()) != null) {
                startActivityForResult(takeVideoIntent, REQUEST_VIDEO_CAPTURE);
                // }
            }
        });

        Button callButton = (Button) root.findViewById(R.id.callButton);
        callButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                callAlertDialog();

                /**
                // Calling a phone number
                Intent callIntent = new Intent(Intent.ACTION_CALL);
                callIntent.setData(Uri.parse("tel:1234567890"));
                if (ActivityCompat.checkSelfPermission(getContext(), Manifest.permission.CALL_PHONE) != PackageManager.PERMISSION_GRANTED) {
                    return;
                }
                startActivity(callIntent);
                 */

                /**
                // Sending an email
                Intent emailIntent = new Intent(Intent.ACTION_SEND);
                emailIntent.setType("message/rfc822");
                emailIntent.putExtra(Intent.EXTRA_EMAIL, new String[]{"doctor@psychHelp.com"});
                emailIntent.putExtra(Intent.EXTRA_SUBJECT, "Mental Health Support at __________");
                emailIntent.putExtra(Intent.EXTRA_TEXT, "Dear Dr. ______," +
                        "\n There's a ____________ at _______________." +
                        "\n Your expertise would be appreciated in resolving this dispute." +
                        "\n \n Best," +
                        "\n \n Floyd Team" +
                        "~ Your AI CCTV Buddy");
                try {
                    startActivity(Intent.createChooser(emailIntent, "Send mail..."));
                } catch (android.content.ActivityNotFoundException ex) {
                    Toast.makeText(getContext(), "There are no email clients installed.", Toast.LENGTH_SHORT).show();
                }
                 */

            }
        });

        return root;
    }

    private void callAlertDialog() {
        AlertDialog.Builder dialog=new AlertDialog.Builder(getActivity());
        dialog.setMessage("Would you like to contact the appropriate emergency services?");
        dialog.setTitle("Confirm Contact");
        dialog.setPositiveButton("YES",
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog,
                                        int which) {
                        Toast.makeText(getActivity().getApplicationContext(),"Emergency services contacted, \n please be patient",Toast.LENGTH_LONG).show();
                    }
                });
        dialog.setNegativeButton("cancel",new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                Toast.makeText(getActivity().getApplicationContext(),"Request Cancelled",Toast.LENGTH_LONG).show();
            }
        });
        AlertDialog alertDialog=dialog.create();
        alertDialog.show();
    }

    static final int REQUEST_VIDEO_CAPTURE = 1;

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent intent) {
        if (requestCode == REQUEST_VIDEO_CAPTURE && resultCode == getActivity().RESULT_OK) {
            Uri videoUri = intent.getData();
            // TODO: determine where this video goes for ML Processing (tflite within app or send to firebase cloud)
            confidenceLevel.setProgress((int) modelResult());
            // TODO: select better levels for diff messages
            if (modelResult() > 80) {
                modelResultInfo.setText("Weapon likely, contact authorities immediately!");
            } else if (modelResult() > 40) {
                modelResultInfo.setText("Potentially dangerous, exercise caution and prepare to contact authorities");
            } else {
                modelResultInfo.setText("Likely non-lethal, contact other resources to help mediate");
            }
        }
    }

    public double modelResult() {
        double confidence = 10;
        // TODO: Actually get the model result
        return confidence;
    }

    // If using tflite model + runnable on mobile
    public FirebaseCustomRemoteModel loadModel() {
        FirebaseCustomRemoteModel remoteModel =
                new FirebaseCustomRemoteModel.Builder("your_model").build();
        FirebaseModelDownloadConditions conditions = new FirebaseModelDownloadConditions.Builder()
                .requireWifi()
                .build();
        FirebaseModelManager.getInstance().download(remoteModel, conditions)
                .addOnSuccessListener(new OnSuccessListener<Void>() {
                    @Override
                    public void onSuccess(Void v) {
                        // Download complete. Depending on your app, you could enable
                        // the ML feature, or switch from the local model to the remote
                        // model, etc.
                    }
                });

        FirebaseModelManager.getInstance().getLatestModelFile(remoteModel)
                .addOnCompleteListener(new OnCompleteListener<File>() {
                    @Override
                    public void onComplete(@NonNull Task<File> task) {
                        File modelFile = task.getResult();
                        if (modelFile != null) {
                            Interpreter interpreter = new Interpreter(modelFile);
                        }
                    }
                });

        return remoteModel;
    }
}