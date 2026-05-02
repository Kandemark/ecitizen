package com.ecitizen.kenya.data.api.models

import com.google.gson.annotations.SerializedName

data class LoginRequest(
    val username: String,
    val password: String
)

data class RegisterRequest(
    val username: String,
    val email: String,
    @SerializedName("first_name") val firstName: String,
    @SerializedName("last_name") val lastName: String,
    val password: String,
    @SerializedName("id_number") val idNumber: String,
    val phone: String,
    val county: Int? = null
)

data class AuthResponse(
    val access: String,
    val refresh: String,
    val user: UserDto?,
    val profile: ProfileDto?
)

data class UserDto(
    val id: Int,
    val username: String,
    val email: String,
    @SerializedName("first_name") val firstName: String,
    @SerializedName("last_name") val lastName: String,
    @SerializedName("date_joined") val dateJoined: String
)

data class ProfileDto(
    val id: String,
    val user: UserDto?,
    @SerializedName("id_number") val idNumber: String,
    @SerializedName("id_type") val idType: String,
    val phone: String,
    val gender: String,
    @SerializedName("date_of_birth") val dateOfBirth: String?,
    val county: Int?,
    @SerializedName("county_name") val countyName: String?,
    @SerializedName("sub_county") val subCounty: Int?,
    @SerializedName("sub_county_name") val subCountyName: String?,
    val ward: Int?,
    @SerializedName("ward_name") val wardName: String?,
    @SerializedName("is_verified") val isVerified: Boolean,
    val role: String,
    val preferences: Map<String, Boolean>?,
    @SerializedName("avatar_url") val avatarUrl: String?
)

data class PaginatedResponse<T>(
    val next: String?,
    val previous: String?,
    val results: List<T>
)
