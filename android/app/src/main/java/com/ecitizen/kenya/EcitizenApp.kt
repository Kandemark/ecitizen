package com.ecitizen.kenya

import android.app.Application
import com.ecitizen.kenya.data.api.RetrofitClient
import com.ecitizen.kenya.BuildConfig

class EcitizenApp : Application() {
    override fun onCreate() {
        super.onCreate()
        RetrofitClient.setBaseUrl(BuildConfig.BASE_URL)
    }
}
