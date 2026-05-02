package com.ecitizen.kenya.data.api

import com.ecitizen.kenya.data.api.models.*
import okhttp3.MultipartBody
import retrofit2.Response
import retrofit2.http.*

interface EcitizenApi {

    // Auth
    @POST("auth/login/")
    suspend fun login(@Body request: LoginRequest): Response<AuthResponse>

    @POST("auth/register/")
    suspend fun register(@Body request: RegisterRequest): Response<AuthResponse>

    // Profile
    @GET("auth/profiles/{id}/")
    suspend fun getProfile(@Path("id") id: String): Response<ProfileDto>

    @PUT("auth/profiles/{id}/")
    suspend fun updateProfile(@Path("id") id: String, @Body profile: ProfileDto): Response<ProfileDto>

    @Multipart
    @POST("auth/profiles/upload_avatar/")
    suspend fun uploadAvatar(@Part avatar: MultipartBody.Part): Response<Map<String, String>>

    // Counties
    @GET("counties/")
    suspend fun getCounties(): Response<PaginatedResponse<CountyDto>>

    @GET("counties/sub-counties/")
    suspend fun getSubCounties(@Query("county") countyCode: String): Response<PaginatedResponse<SubCountyDto>>

    @GET("counties/wards/")
    suspend fun getWards(@Query("sub_county") subCountyId: Int): Response<PaginatedResponse<WardDto>>

    // Services
    @GET("services/")
    suspend fun getServices(): Response<PaginatedResponse<ServiceDto>>

    @GET("services/{id}/")
    suspend fun getServiceDetail(@Path("id") id: Int): Response<ServiceDto>

    // Applications
    @GET("applications/")
    suspend fun getApplications(): Response<PaginatedResponse<ApplicationDto>>

    @POST("applications/")
    suspend fun submitApplication(@Body data: Map<String, Any>): Response<ApplicationDto>

    // Wallet
    @GET("payments/wallet/")
    suspend fun getWallet(): Response<List<WalletDto>>

    @POST("payments/wallet/top_up/")
    suspend fun topUpWallet(@Body data: Map<String, Any>): Response<WalletDto>

    // Payments
    @GET("payments/transactions/")
    suspend fun getTransactions(): Response<PaginatedResponse<PaymentTransactionDto>>

    @POST("payments/transactions/")
    suspend fun createPayment(@Body data: Map<String, Any>): Response<PaymentTransactionDto>

    // Notifications
    @GET("notifications/notifications/")
    suspend fun getNotifications(): Response<PaginatedResponse<NotificationDto>>

    @POST("notifications/notifications/mark_all_read/")
    suspend fun markAllNotificationsRead(): Response<Map<String, String>>

    // Device Tokens (Push Notifications)
    @POST("notifications/device-tokens/")
    suspend fun registerDeviceToken(@Body data: Map<String, String>): Response<Map<String, Any>>
}
