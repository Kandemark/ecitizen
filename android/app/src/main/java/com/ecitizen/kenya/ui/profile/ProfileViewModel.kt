package com.ecitizen.kenya.ui.profile

import android.app.Application
import android.net.Uri
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.ecitizen.kenya.data.api.RetrofitClient
import com.ecitizen.kenya.data.api.models.ProfileDto
import com.ecitizen.kenya.data.local.TokenManager
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.asRequestBody
import java.io.File
import java.io.FileOutputStream

data class ProfileState(
    val isLoading: Boolean = true,
    val isSaving: Boolean = false,
    val profile: ProfileDto? = null,
    val username: String = "",
    val email: String = "",
    val error: String? = null,
    val avatarUploadMessage: String? = null
)

class ProfileViewModel(application: Application) : AndroidViewModel(application) {

    private val api = RetrofitClient.getApi()
    private val tokenManager = TokenManager(application)

    private val _state = MutableStateFlow(ProfileState())
    val state: StateFlow<ProfileState> = _state

    init {
        loadProfile()
    }

    fun loadProfile() {
        viewModelScope.launch {
            _state.value = _state.value.copy(isLoading = true, error = null)
            try {
                val userId = runBlocking { tokenManager.userId.first() } ?: 0
                val username = kotlinx.coroutines.runBlocking { tokenManager.username.first() } ?: ""
                if (userId > 0) {
                    val response = api.getProfile(userId.toString())
                    val email = response.body()?.user?.email ?: ""
                    _state.value = ProfileState(
                        isLoading = false,
                        profile = response.body(),
                        username = username,
                        email = email
                    )
                } else {
                    _state.value = ProfileState(isLoading = false, error = "Not logged in")
                }
            } catch (e: Exception) {
                _state.value = ProfileState(isLoading = false, error = e.localizedMessage ?: "Connection error")
            }
        }
    }

    fun updateProfile(profile: ProfileDto) {
        viewModelScope.launch {
            _state.value = _state.value.copy(isSaving = true)
            try {
                val userId = runBlocking { tokenManager.userId.first() } ?: 0
                if (userId > 0) {
                    api.updateProfile(userId.toString(), profile)
                    _state.value = _state.value.copy(isSaving = false, profile = profile)
                }
            } catch (e: Exception) {
                _state.value = _state.value.copy(isSaving = false, error = e.localizedMessage ?: "Update failed")
            }
        }
    }

    fun uploadAvatar(uri: Uri) {
        viewModelScope.launch {
            try {
                val context = getApplication<Application>()
                val inputStream = context.contentResolver.openInputStream(uri) ?: return@launch
                val file = File(context.cacheDir, "avatar_upload.jpg")
                FileOutputStream(file).use { output -> inputStream.copyTo(output) }
                inputStream.close()

                val requestBody = file.asRequestBody("image/jpeg".toMediaTypeOrNull())
                val part = MultipartBody.Part.createFormData("avatar", file.name, requestBody)
                val response = api.uploadAvatar(part)
                if (response.isSuccessful) {
                    _state.value = _state.value.copy(avatarUploadMessage = "Avatar updated")
                    loadProfile()
                } else {
                    _state.value = _state.value.copy(error = "Avatar upload failed")
                }
            } catch (e: Exception) {
                _state.value = _state.value.copy(error = e.localizedMessage ?: "Upload failed")
            }
        }
    }

    fun logout() {
        viewModelScope.launch {
            tokenManager.clear()
            RetrofitClient.setToken(null)
        }
    }
}
