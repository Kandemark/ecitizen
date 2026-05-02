package com.ecitizen.kenya

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Surface
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.navigation.compose.rememberNavController
import com.ecitizen.kenya.data.api.RetrofitClient
import com.ecitizen.kenya.data.local.TokenManager
import com.ecitizen.kenya.ui.navigation.NavGraph
import com.ecitizen.kenya.ui.theme.ECitizenTheme
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.runBlocking

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val tokenManager = TokenManager(applicationContext)

        // Restore auth state
        val accessToken = runBlocking { tokenManager.accessToken.first() }
        accessToken?.let { RetrofitClient.setToken(it) }
        val loggedIn = runBlocking { tokenManager.isLoggedIn.first() }

        setContent {
            ECitizenTheme {
                Surface(modifier = Modifier.fillMaxSize()) {
                    val navController = rememberNavController()
                    NavGraph(navController = navController, isLoggedIn = loggedIn)
                }
            }
        }
    }
}
