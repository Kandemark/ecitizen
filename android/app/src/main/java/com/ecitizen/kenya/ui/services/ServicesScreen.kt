package com.ecitizen.kenya.ui.services

import androidx.compose.foundation.clickable
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
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.ecitizen.kenya.data.api.models.ServiceDto
import com.ecitizen.kenya.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ServicesScreen(
    onNavigateBack: () -> Unit,
    viewModel: ServicesViewModel = viewModel()
) {
    val state by viewModel.state.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Government Services", fontWeight = FontWeight.Bold) },
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
                    Button(onClick = { viewModel.loadServices() }, colors = ButtonDefaults.buttonColors(containerColor = KenyaGreen)) {
                        Text("Retry")
                    }
                }
            }
        } else {
            // Backdrop: detail view
            if (state.selectedService != null) {
                ServiceDetailSheet(state.selectedService!!, onDismiss = { viewModel.selectService(null) })
            }
            LazyColumn(modifier = Modifier.padding(padding), contentPadding = PaddingValues(16.dp), verticalArrangement = Arrangement.spacedBy(20.dp)) {
                state.categories.forEach { (category, services) ->
                    item {
                        Text(category, fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Gray900)
                        Spacer(Modifier.height(8.dp))
                    }
                    items(services) { service ->
                        ServiceCard(service, onClick = { viewModel.selectService(service) })
                    }
                }
                item { Spacer(Modifier.height(16.dp)) }
            }
        }
    }
}

@Composable
private fun ServiceCard(service: ServiceDto, onClick: () -> Unit) {
    Card(
        modifier = Modifier.fillMaxWidth().clickable { onClick() },
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    ) {
        Row(modifier = Modifier.padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
            Icon(serviceIcon(service.name), null, tint = KenyaGreen, modifier = Modifier.size(32.dp))
            Spacer(Modifier.width(12.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(service.name, fontWeight = FontWeight.Medium, fontSize = 14.sp, color = Gray900)
                if (service.shortDescription != null) {
                    Text(service.shortDescription!!, fontSize = 12.sp, color = Gray500, maxLines = 2, overflow = TextOverflow.Ellipsis)
                }
            }
            Column(horizontalAlignment = Alignment.End) {
                if (service.feeKes != null) {
                    Text("KES ${service.feeKes!!.toLong()}", fontSize = 13.sp, color = KenyaGreen, fontWeight = FontWeight.Medium)
                }
                if (service.processingDays != null) {
                    Text("${service.processingDays} days", fontSize = 11.sp, color = Gray400)
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun ServiceDetailSheet(service: ServiceDto, onDismiss: () -> Unit) {
    AlertDialog(onDismissRequest = onDismiss, title = { Text(service.name, fontWeight = FontWeight.Bold) }, text = {
        Column {
            if (service.description != null) Text(service.description!!, fontSize = 14.sp, color = Gray700)
            Spacer(Modifier.height(12.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                if (service.feeKes != null) AssistChip(onClick = {}, label = { Text("KES ${service.feeKes!!.toLong()}") }, leadingIcon = { Icon(Icons.Default.Payment, null, Modifier.size(16.dp)) })
                if (service.processingDays != null) AssistChip(onClick = {}, label = { Text("${service.processingDays} days") }, leadingIcon = { Icon(Icons.Default.Schedule, null, Modifier.size(16.dp)) })
            }
        }
    }, confirmButton = {
        TextButton(onClick = onDismiss) { Text("Close", color = KenyaGreen) }
    })
}

private fun serviceIcon(name: String): ImageVector = when {
    name.contains("Passport", true) -> Icons.Default.FlightTakeoff
    name.contains("License", true) || name.contains("Driving", true) -> Icons.Default.DirectionsCar
    name.contains("ID", true) || name.contains("Identity", true) -> Icons.Default.CreditCard
    name.contains("Birth", true) -> Icons.Default.Cake
    name.contains("Business", true) || name.contains("Permit", true) -> Icons.Default.Business
    name.contains("Land", true) -> Icons.Default.Terrain
    name.contains("Tax", true) -> Icons.Default.AccountBalance
    name.contains("Visa", true) || name.contains("Travel", true) -> Icons.Default.Language
    name.contains("Marriage", true) -> Icons.Default.Favorite
    name.contains("Health", true) || name.contains("Medical", true) -> Icons.Default.LocalHospital
    name.contains("Education", true) || name.contains("School", true) -> Icons.Default.School
    name.contains("Police", true) || name.contains("Security", true) -> Icons.Default.Gavel
    else -> Icons.Default.Description
}
