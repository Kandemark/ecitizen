package com.ecitizen.kenya.ui.applications

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.ecitizen.kenya.data.api.RetrofitClient
import com.ecitizen.kenya.data.api.models.ApplicationDto
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

data class ApplicationsState(
    val isLoading: Boolean = true,
    val applications: List<ApplicationDto> = emptyList(),
    val error: String? = null
)

class ApplicationsViewModel(application: Application) : AndroidViewModel(application) {

    private val api = RetrofitClient.getApi()

    private val _state = MutableStateFlow(ApplicationsState())
    val state: StateFlow<ApplicationsState> = _state

    init {
        loadApplications()
    }

    fun loadApplications() {
        viewModelScope.launch {
            _state.value = _state.value.copy(isLoading = true, error = null)
            try {
                val response = api.getApplications()
                if (response.isSuccessful) {
                    val apps = response.body()?.results.orEmpty()
                    _state.value = ApplicationsState(isLoading = false, applications = apps)
                } else {
                    _state.value = ApplicationsState(isLoading = false, error = "Failed to load applications")
                }
            } catch (e: Exception) {
                _state.value = ApplicationsState(isLoading = false, error = e.localizedMessage ?: "Connection error")
            }
        }
    }
}
