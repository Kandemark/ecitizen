package com.ecitizen.kenya.ui.wallet

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.ecitizen.kenya.data.api.RetrofitClient
import com.ecitizen.kenya.data.api.models.WalletDto
import com.ecitizen.kenya.data.api.models.WalletTransactionDto
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

data class WalletState(
    val isLoading: Boolean = true,
    val wallet: WalletDto? = null,
    val recentTransactions: List<WalletTransactionDto> = emptyList(),
    val error: String? = null,
    val topUpAmount: String = "",
    val topUpMessage: String? = null
)

class WalletViewModel(application: Application) : AndroidViewModel(application) {

    private val api = RetrofitClient.getApi()

    private val _state = MutableStateFlow(WalletState())
    val state: StateFlow<WalletState> = _state

    init {
        loadWallet()
    }

    fun loadWallet() {
        viewModelScope.launch {
            _state.value = _state.value.copy(isLoading = true, error = null)
            try {
                val response = api.getWallet()
                if (response.isSuccessful) {
                    val wallet = response.body()?.firstOrNull { it.isActive }
                    _state.value = WalletState(
                        isLoading = false,
                        wallet = wallet,
                        recentTransactions = wallet?.recentTransactions.orEmpty()
                    )
                } else {
                    _state.value = WalletState(isLoading = false, error = "Failed to load wallet")
                }
            } catch (e: Exception) {
                _state.value = WalletState(isLoading = false, error = e.localizedMessage ?: "Connection error")
            }
        }
    }

    fun topUp() {
        val amount = _state.value.topUpAmount.toDoubleOrNull() ?: return
        viewModelScope.launch {
            _state.value = _state.value.copy(isLoading = true, error = null)
            try {
                val response = api.topUpWallet(mapOf("amount" to amount))
                if (response.isSuccessful) {
                    _state.value = _state.value.copy(isLoading = false, topUpAmount = "", topUpMessage = "Top-up of KES $amount initiated")
                    loadWallet()
                } else {
                    _state.value = WalletState(isLoading = false, error = "Top-up failed")
                }
            } catch (e: Exception) {
                _state.value = WalletState(isLoading = false, error = e.localizedMessage ?: "Connection error")
            }
        }
    }

    fun setTopUpAmount(amount: String) {
        _state.value = _state.value.copy(topUpAmount = amount)
    }

    fun clearTopUpMessage() {
        _state.value = _state.value.copy(topUpMessage = null)
    }
}
