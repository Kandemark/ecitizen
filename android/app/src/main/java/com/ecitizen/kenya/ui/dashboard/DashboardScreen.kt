package com.ecitizen.kenya.ui.dashboard

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.ecitizen.kenya.data.api.models.ApplicationDto
import com.ecitizen.kenya.data.api.models.NotificationDto
import com.ecitizen.kenya.data.api.models.ServiceDto
import com.ecitizen.kenya.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DashboardScreen(
    onNavigateToServices: () -> Unit,
    onNavigateToApplications: () -> Unit,
    onNavigateToWallet: () -> Unit,
    onNavigateToProfile: () -> Unit,
    onNavigateToOnboarding: () -> Unit,
    onLogout: () -> Unit,
    viewModel: DashboardViewModel = viewModel()
) {
    val state by viewModel.state.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("e-Citizen", fontWeight = FontWeight.Bold) },
                actions = {
                    IconButton(onClick = onNavigateToProfile) { Icon(Icons.Default.Person, "Profile") }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = KenyaGreen,
                    titleContentColor = Color.White,
                    actionIconContentColor = Color.White
                )
            )
        },
        bottomBar = {
            NavigationBar(containerColor = Color.White) {
                NavigationBarItem(selected = true, onClick = {}, icon = { Icon(Icons.Default.Home, "Home") }, label = { Text("Home") })
                NavigationBarItem(selected = false, onClick = onNavigateToServices, icon = { Icon(Icons.Default.Star, "Services") }, label = { Text("Services") })
                NavigationBarItem(selected = false, onClick = onNavigateToApplications, icon = { Icon(Icons.Default.Description, "Apps") }, label = { Text("My Apps") })
                NavigationBarItem(selected = false, onClick = onNavigateToWallet, icon = { Icon(Icons.Default.Wallet, "Wallet") }, label = { Text("Wallet") })
            }
        },
        containerColor = Gray50
    ) { padding ->
        if (state.isLoading) {
            Box(modifier = Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                CircularProgressIndicator(color = KenyaGreen)
            }
        } else if (state.error != null) {
            Box(modifier = Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text(state.error!!, color = ErrorRed, fontSize = 14.sp)
                    Spacer(Modifier.height(12.dp))
                    Button(onClick = { viewModel.loadDashboard() }, colors = ButtonDefaults.buttonColors(containerColor = KenyaGreen)) {
                        Text("Retry")
                    }
                }
            }
        } else {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding)
                    .verticalScroll(rememberScrollState())
            ) {
                // Wallet Balance Card
                WalletBalanceCard(wallet = state.wallet, onNavigateToWallet = onNavigateToWallet)

                Spacer(Modifier.height(20.dp))

                // Quick Links
                Text("Quick Links", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Gray900, modifier = Modifier.padding(horizontal = 16.dp))
                Spacer(Modifier.height(12.dp))
                QuickLinksRow(services = state.popularServices, onNavigateToServices = onNavigateToServices)

                Spacer(Modifier.height(20.dp))

                // Recent Applications
                SectionHeader("Recent Applications", onNavigateToApplications, modifier = Modifier.padding(horizontal = 16.dp))
                Spacer(Modifier.height(8.dp))
                if (state.recentApplications.isEmpty()) {
                    EmptyCard("No applications yet", "Apply for government services to see them here.", modifier = Modifier.padding(horizontal = 16.dp))
                } else {
                    state.recentApplications.forEach { app -> ApplicationCard(app) }
                }

                Spacer(Modifier.height(20.dp))

                // Notifications
                SectionHeader("Notifications", null, modifier = Modifier.padding(horizontal = 16.dp))
                Spacer(Modifier.height(8.dp))
                if (state.notifications.isEmpty()) {
                    EmptyCard("No new notifications", "You're all caught up!", modifier = Modifier.padding(horizontal = 16.dp))
                } else {
                    state.notifications.take(5).forEach { notif -> NotificationCard(notif) }
                }

                Spacer(Modifier.height(24.dp))
            }
        }
    }
}

@Composable
private fun WalletBalanceCard(wallet: com.ecitizen.kenya.data.api.models.WalletDto?, onNavigateToWallet: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp)
            .clickable { onNavigateToWallet() },
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = KenyaGreen),
        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
    ) {
        Column(modifier = Modifier.padding(20.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.AccountBalanceWallet, "Wallet", tint = Color.White, modifier = Modifier.size(24.dp))
                Spacer(Modifier.width(8.dp))
                Text("Wallet Balance", color = Color.White.copy(alpha = 0.85f), fontSize = 14.sp)
            }
            Spacer(Modifier.height(8.dp))
            val balance = "KES %,d".format(wallet?.balance?.toLong() ?: 0)
            Text(balance, color = Color.White, fontSize = 28.sp, fontWeight = FontWeight.Bold)
            if (wallet != null) {
                Spacer(Modifier.height(4.dp))
                Text("ID: ${wallet.walletId}", color = Color.White.copy(alpha = 0.7f), fontSize = 12.sp)
            } else {
                Spacer(Modifier.height(4.dp))
                Text("Create your wallet on onboarding", color = Color.White.copy(alpha = 0.7f), fontSize = 12.sp)
            }
        }
    }
}

@Composable
private fun QuickLinksRow(services: List<ServiceDto>, onNavigateToServices: () -> Unit) {
    LazyRow(contentPadding = PaddingValues(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
        items(services) { service ->
            val icon = serviceIcon(service.name)
            Card(
                modifier = Modifier
                    .width(100.dp)
                    .clickable { onNavigateToServices() },
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
            ) {
                Column(
                    modifier = Modifier.padding(12.dp).fillMaxWidth(),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Icon(icon, null, tint = KenyaGreen, modifier = Modifier.size(28.dp))
                    Spacer(Modifier.height(8.dp))
                    Text(
                        service.name.take(20),
                        fontSize = 11.sp,
                        color = Gray700,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis,
                        lineHeight = 14.sp
                    )
                }
            }
        }
    }
}

@Composable
private fun SectionHeader(title: String, onViewAll: (() -> Unit)?, modifier: Modifier = Modifier) {
    Row(modifier = modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
        Text(title, fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Gray900)
        if (onViewAll != null) {
            TextButton(onClick = onViewAll) {
                Text("View All", color = KenyaGreen, fontSize = 13.sp)
            }
        }
    }
}

@Composable
private fun ApplicationCard(app: ApplicationDto) {
    Card(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 4.dp),
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    ) {
        Row(
            modifier = Modifier.padding(14.dp).fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(app.service?.name ?: "Service #${app.id}", fontWeight = FontWeight.Medium, fontSize = 14.sp, color = Gray900)
                Spacer(Modifier.height(2.dp))
                Text(app.reference, fontSize = 12.sp, color = Gray500)
            }
            StatusChip(app.status)
        }
    }
}

@Composable
private fun StatusChip(status: String) {
    val (bg, fg) = when (status.lowercase()) {
        "approved" -> KenyaGreenLight to KenyaGreen
        "pending" -> Color(0xFFFFF3E0) to WarningAmber
        "rejected" -> Color(0xFFFFEBEE) to ErrorRed
        "completed" -> Color(0xFFE8F5E9) to SuccessGreen
        "processing" -> Color(0xFFE3F2FD) to InfoBlue
        else -> Gray100 to Gray500
    }
    Surface(shape = RoundedCornerShape(20.dp), color = bg) {
        Text(status.replaceFirstChar { it.uppercase() }, modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp), fontSize = 11.sp, color = fg, fontWeight = FontWeight.Medium)
    }
}

@Composable
private fun NotificationCard(notif: NotificationDto) {
    Card(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 4.dp),
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    ) {
        Row(
            modifier = Modifier.padding(14.dp),
            verticalAlignment = Alignment.Top
        ) {
            Icon(
                Icons.Default.Notifications,
                contentDescription = null,
                tint = if (notif.isRead) Gray400 else KenyaGreen,
                modifier = Modifier.size(20.dp)
            )
            Spacer(Modifier.width(10.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(notif.title, fontWeight = FontWeight.Medium, fontSize = 14.sp, color = Gray900)
                Text(notif.message, fontSize = 12.sp, color = Gray500, maxLines = 2, overflow = TextOverflow.Ellipsis)
            }
        }
    }
}

@Composable
private fun EmptyCard(title: String, subtitle: String, modifier: Modifier = Modifier) {
    Card(
        modifier = modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    ) {
        Column(modifier = Modifier.padding(24.dp).fillMaxWidth(), horizontalAlignment = Alignment.CenterHorizontally) {
            Icon(Icons.Default.Info, null, tint = Gray400, modifier = Modifier.size(32.dp))
            Spacer(Modifier.height(8.dp))
            Text(title, color = Gray700, fontSize = 14.sp, fontWeight = FontWeight.Medium)
            Text(subtitle, color = Gray400, fontSize = 12.sp)
        }
    }
}

private fun serviceIcon(name: String): ImageVector = when {
    name.contains("Passport", ignoreCase = true) -> Icons.Default.FlightTakeoff
    name.contains("License", ignoreCase = true) || name.contains("Driving", ignoreCase = true) -> Icons.Default.DirectionsCar
    name.contains("ID", ignoreCase = true) || name.contains("Identity", ignoreCase = true) -> Icons.Default.CreditCard
    name.contains("Birth", ignoreCase = true) -> Icons.Default.Cake
    name.contains("Business", ignoreCase = true) || name.contains("Permit", ignoreCase = true) -> Icons.Default.Business
    name.contains("Land", ignoreCase = true) -> Icons.Default.Terrain
    name.contains("Tax", ignoreCase = true) -> Icons.Default.AccountBalance
    name.contains("Visa", ignoreCase = true) -> Icons.Default.Language
    name.contains("Marriage", ignoreCase = true) -> Icons.Default.Favorite
    name.contains("Health", ignoreCase = true) || name.contains("Medical", ignoreCase = true) -> Icons.Default.LocalHospital
    name.contains("Education", ignoreCase = true) -> Icons.Default.School
    name.contains("Police", ignoreCase = true) -> Icons.Default.Gavel
    else -> Icons.Default.Description
}
