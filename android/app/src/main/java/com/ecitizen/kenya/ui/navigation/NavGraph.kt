package com.ecitizen.kenya.ui.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.ecitizen.kenya.ui.auth.LoginScreen
import com.ecitizen.kenya.ui.auth.RegisterScreen
import com.ecitizen.kenya.ui.dashboard.DashboardScreen
import com.ecitizen.kenya.ui.onboarding.OnboardingScreen
import com.ecitizen.kenya.ui.services.ServicesScreen
import com.ecitizen.kenya.ui.applications.ApplicationsScreen
import com.ecitizen.kenya.ui.wallet.WalletScreen
import com.ecitizen.kenya.ui.profile.ProfileScreen

object Routes {
    const val LOGIN = "login"
    const val REGISTER = "register"
    const val DASHBOARD = "dashboard"
    const val ONBOARDING = "onboarding"
    const val SERVICES = "services"
    const val APPLICATIONS = "applications"
    const val WALLET = "wallet"
    const val PROFILE = "profile"
}

@Composable
fun NavGraph(navController: NavHostController, isLoggedIn: Boolean) {
    val startDestination = if (isLoggedIn) Routes.DASHBOARD else Routes.LOGIN

    NavHost(navController = navController, startDestination = startDestination) {
        composable(Routes.LOGIN) {
            LoginScreen(
                onLoginSuccess = { navController.navigate(Routes.DASHBOARD) { popUpTo(0) } },
                onNavigateToRegister = { navController.navigate(Routes.REGISTER) }
            )
        }
        composable(Routes.REGISTER) {
            RegisterScreen(
                onRegisterSuccess = { navController.navigate(Routes.DASHBOARD) { popUpTo(0) } },
                onNavigateToLogin = { navController.popBackStack() }
            )
        }
        composable(Routes.DASHBOARD) {
            DashboardScreen(
                onNavigateToServices = { navController.navigate(Routes.SERVICES) },
                onNavigateToApplications = { navController.navigate(Routes.APPLICATIONS) },
                onNavigateToWallet = { navController.navigate(Routes.WALLET) },
                onNavigateToProfile = { navController.navigate(Routes.PROFILE) },
                onNavigateToOnboarding = { navController.navigate(Routes.ONBOARDING) },
                onLogout = { navController.navigate(Routes.LOGIN) { popUpTo(0) } }
            )
        }
        composable(Routes.ONBOARDING) {
            OnboardingScreen(
                onComplete = { navController.navigate(Routes.DASHBOARD) { popUpTo(0) } }
            )
        }
        composable(Routes.SERVICES) {
            ServicesScreen(
                onNavigateBack = { navController.popBackStack() }
            )
        }
        composable(Routes.APPLICATIONS) {
            ApplicationsScreen(
                onNavigateBack = { navController.popBackStack() }
            )
        }
        composable(Routes.WALLET) {
            WalletScreen(
                onNavigateBack = { navController.popBackStack() }
            )
        }
        composable(Routes.PROFILE) {
            ProfileScreen(
                onNavigateBack = { navController.popBackStack() },
                onLogout = { navController.navigate(Routes.LOGIN) { popUpTo(0) } }
            )
        }
    }
}
