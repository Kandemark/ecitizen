package com.ecitizen.kenya.ui.dashboard

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.ecitizen.kenya.data.api.RetrofitClient
import com.ecitizen.kenya.data.api.models.*
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

data class DashboardState(
    val isLoading: Boolean = true,
    val wallet: WalletDto? = null,
    val recentApplications: List<ApplicationDto> = emptyList(),
    val notifications: List<NotificationDto> = emptyList(),
    val popularServices: List<ServiceDto> = emptyList(),
    val error: String? = null
)

class DashboardViewModel(application: Application) : AndroidViewModel(application) {

    private val api = RetrofitClient.getApi()

    private val _state = MutableStateFlow(DashboardState())
    val state: StateFlow<DashboardState> = _state

    init {
        loadDashboard()
    }

    fun loadDashboard() {
        viewModelScope.launch {
            _state.value = _state.value.copy(isLoading = true, error = null)
            try {
                val walletResult = runCatching { api.getWallet() }
                val appsResult = runCatching { api.getApplications() }
                val notifResult = runCatching { api.getNotifications() }
                val svcResult = runCatching { api.getServices() }

                val wallet = walletResult.getOrNull()?.body()?.firstOrNull { it.isActive }
                val apps = appsResult.getOrNull()?.body()?.results.orEmpty()
                val notifs = notifResult.getOrNull()?.body()?.results.orEmpty()
                val services = svcResult.getOrNull()?.body()?.results.orEmpty().filter { it.isPopular }

                _state.value = DashboardState(
                    isLoading = false,
                    wallet = wallet,
                    recentApplications = apps.take(5),
                    notifications = notifs.filter { !it.isRead },
                    popularServices = services.take(6)
                )
            } catch (e: Exception) {
                _state.value = _state.value.copy(
                    isLoading = false,
                    error = e.localizedMessage ?: "Failed to load dashboard"
                )
            }
        }
    }

    fun markAllRead() {
        viewModelScope.launch {
            runCatching { api.markAllNotificationsRead() }
        }
    }
}
