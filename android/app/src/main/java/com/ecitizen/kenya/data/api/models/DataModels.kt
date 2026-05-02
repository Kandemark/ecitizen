package com.ecitizen.kenya.data.api.models

import com.google.gson.annotations.SerializedName

data class CountyDto(
    val id: Int,
    val code: String,
    val name: String,
    val capital: String,
    val governor: String,
    val population: Long,
    @SerializedName("area_sqkm") val areaSqKm: Double,
    @SerializedName("sub_counties") val subCounties: List<SubCountyDto>?
)

data class SubCountyDto(
    val id: Int,
    val name: String,
    val code: String,
    val county: Int
)

data class WardDto(
    val id: Int,
    val name: String,
    val code: String,
    @SerializedName("sub_county") val subCounty: Int
)

data class ServiceDto(
    val id: Int,
    val name: String,
    @SerializedName("short_description") val shortDescription: String?,
    val description: String?,
    @SerializedName("fee_kes") val feeKes: Double?,
    @SerializedName("processing_days") val processingDays: Int?,
    @SerializedName("is_active") val isActive: Boolean,
    @SerializedName("is_popular") val isPopular: Boolean,
    val category: Int?,
    val ministry: Int?
)

data class ApplicationDto(
    val id: Int,
    val user: Int,
    val service: ServiceDto?,
    val reference: String,
    val status: String,
    @SerializedName("form_data") val formData: Map<String, Any>?,
    @SerializedName("submitted_at") val submittedAt: String?,
    @SerializedName("completed_at") val completedAt: String?,
    @SerializedName("created_at") val createdAt: String
)

data class WalletDto(
    val id: Int,
    val user: Int,
    @SerializedName("wallet_id") val walletId: String,
    val balance: Double,
    val currency: String,
    @SerializedName("is_active") val isActive: Boolean,
    @SerializedName("recent_transactions") val recentTransactions: List<WalletTransactionDto>?
)

data class WalletTransactionDto(
    val id: Int,
    val wallet: Int,
    @SerializedName("transaction_type") val transactionType: String,
    val amount: Double,
    @SerializedName("balance_before") val balanceBefore: Double,
    @SerializedName("balance_after") val balanceAfter: Double,
    val reference: String,
    val description: String?,
    @SerializedName("created_at") val createdAt: String
)

data class NotificationDto(
    val id: Int,
    val title: String,
    val message: String,
    val channel: String,
    @SerializedName("is_read") val isRead: Boolean,
    @SerializedName("created_at") val createdAt: String
)

data class PaymentTransactionDto(
    val id: Int,
    val amount: Double,
    val currency: String,
    val status: String,
    val reference: String,
    @SerializedName("mpesa_receipt") val mpesaReceipt: String?,
    val description: String?,
    @SerializedName("created_at") val createdAt: String
)

data class EconomicIndicators(
    @SerializedName("inflation_rate") val inflationRate: Double,
    @SerializedName("gdp_growth") val gdpGrowth: Double,
    val population: Long,
    @SerializedName("unemployment_rate") val unemploymentRate: Double,
    @SerializedName("cbr_rate") val cbrRate: Double,
    @SerializedName("last_updated") val lastUpdated: String
)

data class ExchangeRates(
    val USD: Double,
    val EUR: Double,
    val GBP: Double,
    val TZS: Double,
    val UGX: Double,
    val RWF: Double,
    @SerializedName("last_updated") val lastUpdated: String
)
