package com.ecitizen.kenya.ui.services

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.ecitizen.kenya.data.api.RetrofitClient
import com.ecitizen.kenya.data.api.models.ServiceDto
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

data class ServicesState(
    val isLoading: Boolean = true,
    val services: List<ServiceDto> = emptyList(),
    val categories: Map<String, List<ServiceDto>> = emptyMap(),
    val selectedService: ServiceDto? = null,
    val error: String? = null
)

class ServicesViewModel(application: Application) : AndroidViewModel(application) {

    private val api = RetrofitClient.getApi()

    private val _state = MutableStateFlow(ServicesState())
    val state: StateFlow<ServicesState> = _state

    init {
        loadServices()
    }

    fun loadServices() {
        viewModelScope.launch {
            _state.value = _state.value.copy(isLoading = true, error = null)
            try {
                val response = api.getServices()
                if (response.isSuccessful) {
                    val services = response.body()?.results.orEmpty().filter { it.isActive }
                    val categories = services.groupBy { svc ->
                        val name = svc.name
                        when {
                            name.contains("Passport", true) || name.contains("Visa", true) || name.contains("Travel", true) -> "Travel & Immigration"
                            name.contains("License", true) || name.contains("Driving", true) -> "Driving & Transport"
                            name.contains("Birth", true) || name.contains("Death", true) || name.contains("Marriage", true) -> "Civil Registration"
                            name.contains("Business", true) || name.contains("Permit", true) || name.contains("Company", true) -> "Business & Trade"
                            name.contains("Land", true) || name.contains("Title", true) -> "Land & Property"
                            name.contains("Tax", true) || name.contains("Revenue", true) -> "Tax & Revenue"
                            name.contains("Health", true) || name.contains("Medical", true) -> "Health"
                            name.contains("Education", true) || name.contains("School", true) -> "Education"
                            name.contains("Police", true) || name.contains("Security", true) -> "Security & Law"
                            else -> "General Services"
                        }
                    }
                    _state.value = ServicesState(isLoading = false, services = services, categories = categories)
                } else {
                    _state.value = ServicesState(isLoading = false, error = "Failed to load services")
                }
            } catch (e: Exception) {
                _state.value = ServicesState(isLoading = false, error = e.localizedMessage ?: "Connection error")
            }
        }
    }

    fun selectService(service: ServiceDto?) {
        _state.value = _state.value.copy(selectedService = service)
    }
}
