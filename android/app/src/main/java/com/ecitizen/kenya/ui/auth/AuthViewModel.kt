package com.ecitizen.kenya.ui.auth

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.ecitizen.kenya.data.api.RetrofitClient
import com.ecitizen.kenya.data.api.models.LoginRequest
import com.ecitizen.kenya.data.api.models.RegisterRequest
import com.ecitizen.kenya.data.local.TokenManager
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

data class AuthState(
    val isLoading: Boolean = false,
    val isSuccess: Boolean = false,
    val error: String? = null,
    val username: String = ""
)

class AuthViewModel(application: Application) : AndroidViewModel(application) {

    private val tokenManager = TokenManager(application)
    private val api = RetrofitClient.getApi()

    private val _loginState = MutableStateFlow(AuthState())
    val loginState: StateFlow<AuthState> = _loginState

    private val _registerState = MutableStateFlow(AuthState())
    val registerState: StateFlow<AuthState> = _registerState

    fun login(username: String, password: String) {
        viewModelScope.launch {
            _loginState.value = AuthState(isLoading = true, username = username)
            try {
                val response = api.login(LoginRequest(username, password))
                if (response.isSuccessful) {
                    val auth = response.body()!!
                    RetrofitClient.setToken(auth.access)
                    tokenManager.saveTokens(
                        access = auth.access,
                        refresh = auth.refresh,
                        userId = auth.user?.id ?: 0,
                        username = auth.user?.username ?: username
                    )
                    _loginState.value = AuthState(isSuccess = true, username = username)
                } else {
                    _loginState.value = AuthState(error = "Invalid username or password.")
                }
            } catch (e: Exception) {
                _loginState.value = AuthState(error = e.localizedMessage ?: "Connection error. Please try again.")
            }
        }
    }

    fun register(
        username: String, email: String, firstName: String, lastName: String,
        password: String, idNumber: String, phone: String, county: Int?
    ) {
        viewModelScope.launch {
            _registerState.value = AuthState(isLoading = true, username = username)
            try {
                val response = api.register(RegisterRequest(
                    username, email, firstName, lastName, password, idNumber, phone, county
                ))
                if (response.isSuccessful) {
                    val auth = response.body()!!
                    RetrofitClient.setToken(auth.access)
                    tokenManager.saveTokens(
                        access = auth.access,
                        refresh = auth.refresh,
                        userId = auth.user?.id ?: 0,
                        username = auth.user?.username ?: username
                    )
                    _registerState.value = AuthState(isSuccess = true, username = username)
                } else {
                    val errBody = response.errorBody()?.string() ?: "Registration failed."
                    _registerState.value = AuthState(error = errBody)
                }
            } catch (e: Exception) {
                _registerState.value = AuthState(error = e.localizedMessage ?: "Connection error.")
            }
        }
    }
}
