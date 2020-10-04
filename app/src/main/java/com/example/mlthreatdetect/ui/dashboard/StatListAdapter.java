package com.example.mlthreatdetect.ui.dashboard;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import androidx.annotation.NonNull;

import com.example.mlthreatdetect.R;

import org.w3c.dom.Text;

import java.util.ArrayList;

public class StatListAdapter extends ArrayAdapter<Stat> {
    private Context mContext;
    private int mResource;

    public StatListAdapter(@NonNull Context context, int resource, ArrayList<Stat> stats) {
        super(context, resource, stats);
        mContext = context;
        mResource = resource;
    }

    @NonNull
    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        String name = ((Stat) getItem(position)).getName();
        int amount = ((Stat) getItem(position)).getAmount();

        Stat stat = new Stat(name, amount);

        LayoutInflater inflater = LayoutInflater.from(mContext);
        convertView = inflater.inflate(mResource, parent,false);

        TextView sName = (TextView) convertView.findViewById(R.id.textView1);
        TextView sAmount = (TextView) convertView.findViewById(R.id.textView2);

        sName.setText(stat.getName());
        sAmount.setText(String.valueOf(stat.getAmount()));

        return convertView;
    }
}
