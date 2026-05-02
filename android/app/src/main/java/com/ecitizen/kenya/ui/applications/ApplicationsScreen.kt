package com.ecitizen.kenya.ui.applications

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.ecitizen.kenya.data.api.models.ApplicationDto
import com.ecitizen.kenya.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ApplicationsScreen(
    onNavigateBack: () -> Unit,
    viewModel: ApplicationsViewModel = viewModel()
) {
    val state by viewModel.state.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("My Applications", fontWeight = FontWeight.Bold) },
                navigationIcon = { IconButton(onClick = onNavigateBack) { Icon(Icons.Default.ArrowBack, "Back", tint = Color.White) } },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = KenyaGreen, titleContentColor = Color.White)
            )
        }
    ) { padding ->
        if (state.isLoading) {
            Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                CircularProgressIndicator(color = KenyaGreen)
            }
        } else if (state.error != null) {
            Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text(state.error!!, color = ErrorRed, fontSize = 14.sp)
                    Spacer(Modifier.height(12.dp))
                    Button(onClick = { viewModel.loadApplications() }, colors = ButtonDefaults.buttonColors(containerColor = KenyaGreen)) {
                        Text("Retry")
                    }
                }
            }
        } else if (state.applications.isEmpty()) {
            Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Icon(Icons.Default.Description, null, tint = Gray400, modifier = Modifier.size(64.dp))
                    Spacer(Modifier.height(12.dp))
                    Text("No Applications Yet", fontWeight = FontWeight.Bold, fontSize = 18.sp, color = Gray700)
                    Spacer(Modifier.height(4.dp))
                    Text("Your submitted applications will appear here.", fontSize = 14.sp, color = Gray500)
                }
            }
        } else {
            LazyColumn(
                modifier = Modifier.padding(padding),
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                item {
                    Text("${state.applications.size} application${if (state.applications.size != 1) "s" else ""}", color = Gray500, fontSize = 13.sp)
                    Spacer(Modifier.height(4.dp))
                }
                items(state.applications) { app ->
                    ApplicationCard(app)
                }
                item { Spacer(Modifier.height(16.dp)) }
            }
        }
    }
}

@Composable
private fun ApplicationCard(app: ApplicationDto) {
    Card(
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    Icons.Default.Description,
                    null,
                    tint = KenyaGreen,
                    modifier = Modifier.size(24.dp)
                )
                Spacer(Modifier.width(10.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        app.service?.name ?: "Application #${app.id}",
                        fontWeight = FontWeight.Medium,
                        fontSize = 15.sp,
                        color = Gray900
                    )
                    Spacer(Modifier.height(2.dp))
                    Text(app.reference, fontSize = 12.sp, color = Gray500)
                }
                StatusChip(app.status)
            }
            Spacer(Modifier.height(10.dp))
            Divider(color = Gray100)
            Spacer(Modifier.height(10.dp))
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                DetailChip("Submitted", app.submittedAt?.take(10) ?: app.createdAt.take(10), Icons.Default.CalendarToday)
                if (app.completedAt != null) {
                    DetailChip("Completed", app.completedAt!!.take(10), Icons.Default.CheckCircle)
                }
            }
        }
    }
}

@Composable
private fun StatusChip(status: String) {
    val (bg, fg, icon) = when (status.lowercase()) {
        "approved" -> Triple(KenyaGreenLight, KenyaGreen, Icons.Default.CheckCircle)
        "pending" -> Triple(Color(0xFFFFF3E0), WarningAmber, Icons.Default.HourglassEmpty)
        "rejected" -> Triple(Color(0xFFFFEBEE), ErrorRed, Icons.Default.Cancel)
        "completed" -> Triple(Color(0xFFE8F5E9), SuccessGreen, Icons.Default.TaskAlt)
        "processing" -> Triple(Color(0xFFE3F2FD), InfoBlue, Icons.Default.Refresh)
        "submitted" -> Triple(Color(0xFFF3E5F5), Color(0xFF7B1FA2), Icons.Default.Send)
        else -> Triple(Gray100, Gray500, Icons.Default.Info)
    }
    Surface(shape = RoundedCornerShape(20.dp), color = bg) {
        Row(modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp), verticalAlignment = Alignment.CenterVertically) {
            Icon(icon, null, tint = fg, modifier = Modifier.size(14.dp))
            Spacer(Modifier.width(4.dp))
            Text(status.replaceFirstChar { it.uppercase() }, fontSize = 11.sp, color = fg, fontWeight = FontWeight.Medium)
        }
    }
}

@Composable
private fun DetailChip(label: String, value: String, icon: androidx.compose.ui.graphics.vector.ImageVector) {
    Row(verticalAlignment = Alignment.CenterVertically) {
        Icon(icon, null, tint = Gray400, modifier = Modifier.size(14.dp))
        Spacer(Modifier.width(4.dp))
        Text("$label: ", fontSize = 11.sp, color = Gray400)
        Text(value, fontSize = 11.sp, color = Gray700, fontWeight = FontWeight.Medium)
    }
}
