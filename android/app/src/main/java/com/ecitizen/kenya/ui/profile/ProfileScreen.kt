package com.ecitizen.kenya.ui.profile

import android.app.Activity
import android.content.Intent
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import coil.compose.AsyncImage
import com.ecitizen.kenya.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProfileScreen(
    onNavigateBack: () -> Unit,
    onLogout: () -> Unit,
    viewModel: ProfileViewModel = viewModel()
) {
    val state by viewModel.state.collectAsState()
    val context = LocalContext.current

    val imagePicker = rememberLauncherForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
        if (result.resultCode == Activity.RESULT_OK) {
            result.data?.data?.let { uri ->
                viewModel.uploadAvatar(uri)
            }
        }
    }

    LaunchedEffect(Unit) { viewModel.loadProfile() }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Profile", fontWeight = FontWeight.Bold) },
                navigationIcon = { IconButton(onClick = onNavigateBack) { Icon(Icons.Default.ArrowBack, "Back", tint = Color.White) } },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = KenyaGreen, titleContentColor = Color.White)
            )
        }
    ) { padding ->
        if (state.isLoading) {
            Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                CircularProgressIndicator(color = KenyaGreen)
            }
        } else if (state.error != null && state.profile == null) {
            Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text(state.error!!, color = ErrorRed, fontSize = 14.sp)
                    Spacer(Modifier.height(12.dp))
                    Button(onClick = { viewModel.loadProfile() }, colors = ButtonDefaults.buttonColors(containerColor = KenyaGreen)) {
                        Text("Retry")
                    }
                }
            }
        } else {
            val profile = state.profile
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding)
                    .verticalScroll(rememberScrollState()),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Spacer(Modifier.height(24.dp))

                // Avatar
                Box(contentAlignment = Alignment.BottomEnd) {
                    if (profile?.avatarUrl != null) {
                        AsyncImage(
                            model = profile.avatarUrl,
                            contentDescription = "Avatar",
                            modifier = Modifier.size(100.dp).clip(CircleShape),
                            contentScale = ContentScale.Crop
                        )
                    } else {
                        Surface(
                            modifier = Modifier.size(100.dp),
                            shape = CircleShape,
                            color = KenyaGreenLight
                        ) {
                            Icon(
                                Icons.Default.Person,
                                null,
                                tint = KenyaGreen,
                                modifier = Modifier.padding(24.dp)
                            )
                        }
                    }
                    Surface(
                        modifier = Modifier.size(32.dp).clickable {
                            val intent = Intent(Intent.ACTION_PICK).apply { type = "image/*" }
                            imagePicker.launch(intent)
                        },
                        shape = CircleShape,
                        color = KenyaGreen
                    ) {
                        Icon(Icons.Default.CameraAlt, "Upload", tint = Color.White, modifier = Modifier.padding(6.dp))
                    }
                }

                Spacer(Modifier.height(12.dp))
                Text("@${state.username}", fontWeight = FontWeight.Bold, fontSize = 20.sp, color = Gray900)
                if (state.email.isNotBlank()) Text(state.email, fontSize = 14.sp, color = Gray500)

                Spacer(Modifier.height(24.dp))

                // Profile Details Card
                Card(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp), shape = RoundedCornerShape(16.dp), colors = CardDefaults.cardColors(containerColor = Color.White), elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)) {
                    Column(modifier = Modifier.padding(20.dp)) {
                        Text("Account Details", fontWeight = FontWeight.Bold, fontSize = 16.sp, color = Gray900)
                        Spacer(Modifier.height(16.dp))

                        profile?.let { p ->
                            ProfileRow("ID Number", p.idNumber, Icons.Default.Badge)
                            ProfileRow("ID Type", p.idType.replace("_", " ").replaceFirstChar { it.uppercase() }, Icons.Default.CreditCard)
                            ProfileRow("Phone", p.phone, Icons.Default.Phone)
                            ProfileRow("Gender", p.gender.ifEmpty { "Not set" }, Icons.Default.People)
                            ProfileRow("Date of Birth", p.dateOfBirth ?: "Not set", Icons.Default.CalendarToday)
                            ProfileRow("County", p.countyName ?: "Not set", Icons.Default.LocationOn)
                            ProfileRow("Sub-County", p.subCountyName ?: "Not set", Icons.Default.Map)
                            ProfileRow("Ward", p.wardName ?: "Not set", Icons.Default.PinDrop)
                            ProfileRow("Verified", if (p.isVerified) "Yes" else "Pending", if (p.isVerified) Icons.Default.Verified else Icons.Default.Pending)
                        }
                    }
                }

                Spacer(Modifier.height(20.dp))

                // Verification Card (if not verified)
                if (profile != null && !profile.isVerified) {
                    Card(
                        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp),
                        shape = RoundedCornerShape(12.dp),
                        colors = CardDefaults.cardColors(containerColor = Color(0xFFFFF8E1)),
                        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
                    ) {
                        Row(modifier = Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.Info, null, tint = WarningAmber)
                            Spacer(Modifier.width(12.dp))
                            Column(modifier = Modifier.weight(1f)) {
                                Text("Account not verified", fontWeight = FontWeight.Medium, color = Gray900)
                                Text("Complete onboarding to verify your account.", fontSize = 12.sp, color = Gray500)
                            }
                        }
                    }
                    Spacer(Modifier.height(20.dp))
                }

                // Logout
                Button(
                    onClick = {
                        viewModel.logout()
                        onLogout()
                    },
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp).height(50.dp),
                    shape = RoundedCornerShape(12.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = KenyaRed)
                ) {
                    Icon(Icons.Default.Logout, null, tint = Color.White)
                    Spacer(Modifier.width(8.dp))
                    Text("Sign Out", fontWeight = FontWeight.SemiBold)
                }

                Spacer(Modifier.height(40.dp))
            }
        }
    }
}

@Composable
private fun ProfileRow(label: String, value: String, icon: androidx.compose.ui.graphics.vector.ImageVector) {
    Row(
        modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(icon, null, tint = Gray400, modifier = Modifier.size(18.dp))
        Spacer(Modifier.width(12.dp))
        Column {
            Text(label, fontSize = 11.sp, color = Gray400)
            Text(value, fontSize = 14.sp, color = Gray900, fontWeight = FontWeight.Medium)
        }
    }
    Divider(color = Gray100)
}
