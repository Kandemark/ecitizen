package com.ecitizen.kenya.ui.onboarding

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.ecitizen.kenya.data.api.RetrofitClient
import com.ecitizen.kenya.data.api.models.*
import com.ecitizen.kenya.data.local.TokenManager
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking

data class OnboardingState(
    val currentStep: Int = 1,
    val totalSteps: Int = 10,
    val isLoading: Boolean = false,
    val isComplete: Boolean = false,
    val error: String? = null,
    // Step 2: ID type
    val idType: String = "national_id",
    // Step 3: Demographics
    val gender: String = "",
    val dateOfBirth: String = "",
    // Step 4: Occupation
    val occupation: String = "",
    val educationLevel: String = "",
    // Step 5: Location
    val counties: List<CountyDto> = emptyList(),
    val selectedCounty: CountyDto? = null,
    val subCounties: List<SubCountyDto> = emptyList(),
    val selectedSubCounty: SubCountyDto? = null,
    val wards: List<WardDto> = emptyList(),
    val selectedWard: WardDto? = null,
    // Step 6: Interests
    val selectedServices: Set<Int> = emptySet(),
    val services: List<ServiceDto> = emptyList(),
    // Step 7: Notification preferences
    val emailNotifications: Boolean = true,
    val smsNotifications: Boolean = true,
    val pushNotifications: Boolean = true,
    // Step 8: Transaction PIN
    val transactionPin: String = "",
    val confirmPin: String = "",
    // Step 9: Privacy
    val agreeTerms: Boolean = false,
    val agreePrivacy: Boolean = false
)

class OnboardingViewModel(application: Application) : AndroidViewModel(application) {

    private val api = RetrofitClient.getApi()
    private val tokenManager = TokenManager(application)

    private val _state = MutableStateFlow(OnboardingState())
    val state: StateFlow<OnboardingState> = _state

    init {
        loadCounties()
        loadServices()
    }

    fun nextStep() {
        val current = _state.value.currentStep
        if (current < 10) _state.value = _state.value.copy(currentStep = current + 1, error = null)
    }

    fun previousStep() {
        val current = _state.value.currentStep
        if (current > 1) _state.value = _state.value.copy(currentStep = current - 1, error = null)
    }

    fun updateIdType(type: String) { _state.value = _state.value.copy(idType = type) }
    fun updateGender(gender: String) { _state.value = _state.value.copy(gender = gender) }
    fun updateDateOfBirth(dob: String) { _state.value = _state.value.copy(dateOfBirth = dob) }
    fun updateOccupation(occ: String) { _state.value = _state.value.copy(occupation = occ) }
    fun updateEducation(edu: String) { _state.value = _state.value.copy(educationLevel = edu) }
    fun updateTransactionPin(pin: String) { _state.value = _state.value.copy(transactionPin = pin) }
    fun updateConfirmPin(pin: String) { _state.value = _state.value.copy(confirmPin = pin) }
    fun toggleService(serviceId: Int) {
        val set = _state.value.selectedServices.toMutableSet()
        if (serviceId in set) set.remove(serviceId) else set.add(serviceId)
        _state.value = _state.value.copy(selectedServices = set)
    }
    fun toggleEmailNotifications() { _state.value = _state.value.copy(emailNotifications = !_state.value.emailNotifications) }
    fun toggleSmsNotifications() { _state.value = _state.value.copy(smsNotifications = !_state.value.smsNotifications) }
    fun togglePushNotifications() { _state.value = _state.value.copy(pushNotifications = !_state.value.pushNotifications) }
    fun toggleAgreeTerms() { _state.value = _state.value.copy(agreeTerms = !_state.value.agreeTerms) }
    fun toggleAgreePrivacy() { _state.value = _state.value.copy(agreePrivacy = !_state.value.agreePrivacy) }

    fun selectCounty(county: CountyDto) {
        _state.value = _state.value.copy(selectedCounty = county, selectedSubCounty = null, selectedWard = null, wards = emptyList())
        loadSubCounties(county.code)
    }

    fun selectSubCounty(subCounty: SubCountyDto) {
        _state.value = _state.value.copy(selectedSubCounty = subCounty, selectedWard = null)
        loadWards(subCounty.id)
    }

    fun selectWard(ward: WardDto) { _state.value = _state.value.copy(selectedWard = ward) }

    fun complete() {
        viewModelScope.launch {
            _state.value = _state.value.copy(isLoading = true)
            try {
                val userId = runBlocking { tokenManager.userId.first() } ?: 0
                if (userId > 0) {
                    val profile = api.getProfile(userId.toString()).body()
                    if (profile != null) {
                        val updated = profile.copy(
                            idType = _state.value.idType,
                            gender = _state.value.gender,
                            dateOfBirth = _state.value.dateOfBirth.ifEmpty { null },
                            county = _state.value.selectedCounty?.id,
                            subCounty = _state.value.selectedSubCounty?.id,
                            ward = _state.value.selectedWard?.id,
                            preferences = mapOf(
                                "email_notifications" to _state.value.emailNotifications,
                                "sms_notifications" to _state.value.smsNotifications,
                                "push_notifications" to _state.value.pushNotifications
                            )
                        )
                        api.updateProfile(userId.toString(), updated)
                    }
                }
                _state.value = _state.value.copy(isLoading = false, isComplete = true, currentStep = 10)
            } catch (e: Exception) {
                _state.value = _state.value.copy(isLoading = false, error = e.localizedMessage ?: "Failed")
            }
        }
    }

    private fun loadCounties() {
        viewModelScope.launch {
            runCatching {
                api.getCounties().body()?.results
            }.onSuccess { counties ->
                _state.value = _state.value.copy(counties = counties ?: emptyList())
            }
        }
    }

    private fun loadSubCounties(countyCode: String) {
        viewModelScope.launch {
            runCatching {
                api.getSubCounties(countyCode).body()?.results
            }.onSuccess { subCounties ->
                _state.value = _state.value.copy(subCounties = subCounties ?: emptyList())
            }
        }
    }

    private fun loadWards(subCountyId: Int) {
        viewModelScope.launch {
            runCatching {
                api.getWards(subCountyId).body()?.results
            }.onSuccess { wards ->
                _state.value = _state.value.copy(wards = wards ?: emptyList())
            }
        }
    }

    private fun loadServices() {
        viewModelScope.launch {
            runCatching {
                api.getServices().body()?.results
            }.onSuccess { services ->
                _state.value = _state.value.copy(services = services ?: emptyList())
            }
        }
    }
}
