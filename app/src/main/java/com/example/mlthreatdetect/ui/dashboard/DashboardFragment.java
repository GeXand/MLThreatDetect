package com.example.mlthreatdetect.ui.dashboard;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.ListFragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProviders;

import com.example.mlthreatdetect.MainActivity;
import com.example.mlthreatdetect.R;

import java.util.ArrayList;

public class DashboardFragment extends Fragment {

    private View root = null;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {

        root = inflater.inflate(R.layout.fragment_dashboard, container, false);

        ListView statSummary = (ListView) root.findViewById(R.id.list);

        // TODO: Store/get info from database
        ArrayList<Stat> stats = new ArrayList<Stat>();
        stats.add(new Stat("Foot Traffic", 1000));
        stats.add(new Stat("Store Visitors", 90));
        stats.add(new Stat("Purchases", 40));
        stats.add(new Stat("Lost Items", 3));
        StatListAdapter adapter = new StatListAdapter(getActivity(), R.layout.adapter_view_layout, stats);

        statSummary.setAdapter(adapter);

        return root;
    }

    public void onActivityCreated(Bundle savedInstanceState)
    {
        super.onActivityCreated(savedInstanceState);
    }
}