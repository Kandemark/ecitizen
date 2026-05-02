package com.ecitizen.kenya.ui.onboarding

import androidx.compose.animation.*
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.ecitizen.kenya.data.api.models.CountyDto
import com.ecitizen.kenya.data.api.models.SubCountyDto
import com.ecitizen.kenya.data.api.models.WardDto
import com.ecitizen.kenya.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun OnboardingScreen(
    onComplete: () -> Unit,
    viewModel: OnboardingViewModel = viewModel()
) {
    val state by viewModel.state.collectAsState()

    LaunchedEffect(state.isComplete) {
        if (state.isComplete) onComplete()
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Setup Profile", fontWeight = FontWeight.Bold) },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = KenyaGreen, titleContentColor = Color.White),
                navigationIcon = {
                    if (state.currentStep > 1) IconButton(onClick = { viewModel.previousStep() }) {
                        Icon(Icons.Default.ArrowBack, "Back", tint = Color.White)
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
        ) {
            // Progress bar
            LinearProgressIndicator(
                progress = state.currentStep.toFloat() / state.totalSteps,
                modifier = Modifier.fillMaxWidth().height(4.dp),
                color = KenyaGreen,
                trackColor = Gray200,
            )
            Text(
                "Step ${state.currentStep} of ${state.totalSteps}",
                modifier = Modifier.padding(16.dp),
                fontSize = 13.sp,
                color = Gray500
            )

            state.error?.let {
                Text(it, color = ErrorRed, fontSize = 14.sp, modifier = Modifier.padding(horizontal = 16.dp, vertical = 4.dp))
            }

            AnimatedContent(targetState = state.currentStep, transitionSpec = {
                fadeIn() + slideInHorizontally { it / 4 } togetherWith fadeOut() + slideOutHorizontally { -it / 4 }
            }) { step ->
                Column(modifier = Modifier.padding(16.dp)) {
                    when (step) {
                        1 -> StepWelcome()
                        2 -> StepIdType(state.idType, viewModel::updateIdType)
                        3 -> StepDemographics(state.gender, state.dateOfBirth, viewModel::updateGender, viewModel::updateDateOfBirth)
                        4 -> StepOccupation(state.occupation, state.educationLevel, viewModel::updateOccupation, viewModel::updateEducation)
                        5 -> StepLocation(state, viewModel::selectCounty, viewModel::selectSubCounty, viewModel::selectWard)
                        6 -> StepInterests(state, viewModel::toggleService)
                        7 -> StepNotifications(state, viewModel::toggleEmailNotifications, viewModel::toggleSmsNotifications, viewModel::togglePushNotifications)
                        8 -> StepPin(state.transactionPin, state.confirmPin, viewModel::updateTransactionPin, viewModel::updateConfirmPin)
                        9 -> StepPrivacy(state.agreeTerms, state.agreePrivacy, viewModel::toggleAgreeTerms, viewModel::toggleAgreePrivacy)
                        10 -> StepCompletion(viewModel::complete, state.isLoading)
                    }
                }
            }

            if (state.currentStep < 10) {
                Spacer(Modifier.height(16.dp))
                Button(
                    onClick = { viewModel.nextStep() },
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp).height(50.dp),
                    shape = RoundedCornerShape(12.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = KenyaGreen),
                    enabled = canAdvance(state)
                ) {
                    Text("Continue", fontWeight = FontWeight.SemiBold)
                }
                Spacer(Modifier.height(32.dp))
            }
        }
    }
}

private fun canAdvance(state: OnboardingState): Boolean = when (state.currentStep) {
    3 -> state.gender.isNotBlank() && state.dateOfBirth.isNotBlank()
    4 -> state.occupation.isNotBlank()
    5 -> state.selectedCounty != null && state.selectedSubCounty != null && state.selectedWard != null
    8 -> state.transactionPin.length >= 4 && state.transactionPin == state.confirmPin
    9 -> state.agreeTerms && state.agreePrivacy
    else -> true
}

@Composable
private fun StepWelcome() {
    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.fillMaxWidth()) {
        Icon(Icons.Default.WavingHand, null, tint = KenyaGreen, modifier = Modifier.size(64.dp))
        Spacer(Modifier.height(16.dp))
        Text("Welcome!", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = Gray900)
        Spacer(Modifier.height(8.dp))
        Text("Let's set up your e-Citizen profile.\nFollow the steps to unlock all government services.", fontSize = 14.sp, color = Gray500, lineHeight = 22.sp)
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun StepIdType(selected: String, onSelect: (String) -> Unit) {
    Text("Select your ID type", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = Gray900)
    Spacer(Modifier.height(8.dp))
    Text("This helps us verify your identity across government services.", fontSize = 14.sp, color = Gray500)
    Spacer(Modifier.height(20.dp))
    val options = listOf(
        "national_id" to "National ID" to "Kenyan National ID Card",
        "passport" to "Passport" to "Valid Kenyan Passport",
        "alien_id" to "Alien ID" to "Foreign Resident ID",
        "birth_cert" to "Birth Certificate" to "Official Birth Certificate"
    )
    options.forEach { (pair, desc) ->
        val (value, label) = pair
        Card(
            modifier = Modifier.fillMaxWidth().padding(vertical = 6.dp).clickable { onSelect(value) },
            shape = RoundedCornerShape(12.dp),
            border = if (selected == value) androidx.compose.foundation.BorderStroke(2.dp, KenyaGreen) else null,
            colors = CardDefaults.cardColors(containerColor = if (selected == value) KenyaGreenLight else Color.White),
            elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
        ) {
            Row(modifier = Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                RadioButton(selected = selected == value, onClick = { onSelect(value) }, colors = RadioButtonDefaults.colors(selectedColor = KenyaGreen))
                Spacer(Modifier.width(8.dp))
                Column { Text(label, fontWeight = FontWeight.Medium, color = Gray900); Text(desc, fontSize = 12.sp, color = Gray500) }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun StepDemographics(gender: String, dob: String, onGender: (String) -> Unit, onDob: (String) -> Unit) {
    Text("Personal Details", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = Gray900)
    Spacer(Modifier.height(16.dp))
    Text("Gender", fontWeight = FontWeight.Medium, color = Gray700, fontSize = 14.sp)
    Spacer(Modifier.height(8.dp))
    Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
        listOf("Male" to Icons.Default.Male, "Female" to Icons.Default.Female).forEach { (label, icon) ->
            FilterChip(
                selected = gender == label,
                onClick = { onGender(label) },
                label = { Text(label) },
                leadingIcon = { Icon(icon, null, Modifier.size(16.dp)) },
                colors = FilterChipDefaults.filterChipColors(selectedContainerColor = KenyaGreenLight)
            )
        }
    }
    Spacer(Modifier.height(16.dp))
    OutlinedTextField(
        value = dob, onValueChange = onDob,
        label = { Text("Date of Birth (YYYY-MM-DD)") },
        modifier = Modifier.fillMaxWidth(), singleLine = true,
        colors = OutlinedTextFieldDefaults.colors(focusedBorderColor = KenyaGreen)
    )
}

@Composable
private fun StepOccupation(occupation: String, education: String, onOcc: (String) -> Unit, onEdu: (String) -> Unit) {
    Text("Occupation & Education", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = Gray900)
    Spacer(Modifier.height(16.dp))
    OutlinedTextField(
        value = occupation, onValueChange = onOcc,
        label = { Text("Occupation") },
        modifier = Modifier.fillMaxWidth(), singleLine = true,
        colors = OutlinedTextFieldDefaults.colors(focusedBorderColor = KenyaGreen)
    )
    Spacer(Modifier.height(12.dp))
    Text("Education Level", fontWeight = FontWeight.Medium, color = Gray700, fontSize = 14.sp)
    Spacer(Modifier.height(8.dp))
    val levels = listOf("Primary", "Secondary", "Diploma", "Bachelor's", "Master's", "Doctorate")
    Column {
        levels.forEach { level ->
            Row(modifier = Modifier.clickable { onEdu(level) }.padding(vertical = 6.dp), verticalAlignment = Alignment.CenterVertically) {
                RadioButton(selected = education == level, onClick = { onEdu(level) }, colors = RadioButtonDefaults.colors(selectedColor = KenyaGreen))
                Spacer(Modifier.width(4.dp))
                Text(level, color = Gray900)
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun StepLocation(state: OnboardingState, onCounty: (CountyDto) -> Unit, onSubCounty: (SubCountyDto) -> Unit, onWard: (WardDto) -> Unit) {
    Text("Location", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = Gray900)
    Spacer(Modifier.height(8.dp))
    Text("Select your county, sub-county, and ward.", fontSize = 14.sp, color = Gray500)
    Spacer(Modifier.height(16.dp))

    // County dropdown
    var countyExpanded by remember { mutableStateOf(false) }
    ExposedDropdownMenuBox(expanded = countyExpanded, onExpandedChange = { countyExpanded = it }) {
        OutlinedTextField(
            value = state.selectedCounty?.name ?: "",
            onValueChange = {},
            readOnly = true,
            label = { Text("County") },
            modifier = Modifier.fillMaxWidth().menuAnchor(),
            trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = countyExpanded) },
            colors = OutlinedTextFieldDefaults.colors(focusedBorderColor = KenyaGreen)
        )
        ExposedDropdownMenu(expanded = countyExpanded, onDismissRequest = { countyExpanded = false }) {
            state.counties.forEach { county ->
                DropdownMenuItem(text = { Text(county.name) }, onClick = { onCounty(county); countyExpanded = false })
            }
        }
    }
    Spacer(Modifier.height(12.dp))

    // Sub-County
    var scExpanded by remember { mutableStateOf(false) }
    ExposedDropdownMenuBox(expanded = scExpanded, onExpandedChange = { scExpanded = it }) {
        OutlinedTextField(
            value = state.selectedSubCounty?.name ?: "",
            onValueChange = {},
            readOnly = true,
            label = { Text("Sub-County") },
            modifier = Modifier.fillMaxWidth().menuAnchor(),
            trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = scExpanded) },
            enabled = state.selectedCounty != null,
            colors = OutlinedTextFieldDefaults.colors(focusedBorderColor = KenyaGreen)
        )
        ExposedDropdownMenu(expanded = scExpanded, onDismissRequest = { scExpanded = false }) {
            state.subCounties.forEach { sc ->
                DropdownMenuItem(text = { Text(sc.name) }, onClick = { onSubCounty(sc); scExpanded = false })
            }
        }
    }
    Spacer(Modifier.height(12.dp))

    // Ward
    var wardExpanded by remember { mutableStateOf(false) }
    ExposedDropdownMenuBox(expanded = wardExpanded, onExpandedChange = { wardExpanded = it }) {
        OutlinedTextField(
            value = state.selectedWard?.name ?: "",
            onValueChange = {},
            readOnly = true,
            label = { Text("Ward") },
            modifier = Modifier.fillMaxWidth().menuAnchor(),
            trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = wardExpanded) },
            enabled = state.selectedSubCounty != null,
            colors = OutlinedTextFieldDefaults.colors(focusedBorderColor = KenyaGreen)
        )
        ExposedDropdownMenu(expanded = wardExpanded, onDismissRequest = { wardExpanded = false }) {
            state.wards.forEach { ward ->
                DropdownMenuItem(text = { Text(ward.name) }, onClick = { onWard(ward); wardExpanded = false })
            }
        }
    }
}

@Composable
private fun StepInterests(state: OnboardingState, onToggle: (Int) -> Unit) {
    Text("Services of Interest", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = Gray900)
    Spacer(Modifier.height(8.dp))
    Text("Select services you might use. We'll personalize your dashboard.", fontSize = 14.sp, color = Gray500)
    Spacer(Modifier.height(16.dp))
    state.services.forEach { svc ->
        Card(
            modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp).clickable { onToggle(svc.id) },
            shape = RoundedCornerShape(10.dp),
            border = if (svc.id in state.selectedServices) androidx.compose.foundation.BorderStroke(2.dp, KenyaGreen) else null,
            colors = CardDefaults.cardColors(containerColor = if (svc.id in state.selectedServices) KenyaGreenLight else Color.White),
            elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
        ) {
            Row(modifier = Modifier.padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
                Checkbox(checked = svc.id in state.selectedServices, onCheckedChange = { onToggle(svc.id) }, colors = CheckboxDefaults.colors(checkedColor = KenyaGreen))
                Spacer(Modifier.width(8.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Text(svc.name, fontWeight = FontWeight.Medium, color = Gray900, fontSize = 14.sp)
                    if (svc.shortDescription != null) Text(svc.shortDescription!!, fontSize = 12.sp, color = Gray500)
                }
                if (svc.feeKes != null) Text("KES ${svc.feeKes!!.toLong()}", fontSize = 12.sp, color = KenyaGreen, fontWeight = FontWeight.Medium)
            }
        }
    }
}

@Composable
private fun StepNotifications(state: OnboardingState, onEmail: () -> Unit, onSms: () -> Unit, onPush: () -> Unit) {
    Text("Notification Preferences", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = Gray900)
    Spacer(Modifier.height(8.dp))
    Text("Choose how you'd like to receive updates about your applications.", fontSize = 14.sp, color = Gray500)
    Spacer(Modifier.height(20.dp))
    NotifToggle("Email Notifications", "Receive updates via email", Icons.Default.Email, state.emailNotifications, onEmail)
    NotifToggle("SMS Notifications", "Receive updates via SMS to your phone", Icons.Default.Sms, state.smsNotifications, onSms)
    NotifToggle("Push Notifications", "Receive updates in the mobile app", Icons.Default.Notifications, state.pushNotifications, onPush)
}

@Composable
private fun NotifToggle(title: String, desc: String, icon: ImageVector, checked: Boolean, onToggle: () -> Unit) {
    Card(
        modifier = Modifier.fillMaxWidth().padding(vertical = 6.dp),
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    ) {
        Row(modifier = Modifier.padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
            Icon(icon, null, tint = KenyaGreen, modifier = Modifier.size(24.dp))
            Spacer(Modifier.width(12.dp))
            Column(modifier = Modifier.weight(1f)) { Text(title, fontWeight = FontWeight.Medium, color = Gray900); Text(desc, fontSize = 12.sp, color = Gray500) }
            Switch(checked = checked, onCheckedChange = { onToggle() }, colors = SwitchDefaults.colors(checkedTrackColor = KenyaGreen))
        }
    }
}

@Composable
private fun StepPin(pin: String, confirmPin: String, onPin: (String) -> Unit, onConfirm: (String) -> Unit) {
    Text("Set Transaction PIN", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = Gray900)
    Spacer(Modifier.height(8.dp))
    Text("Create a secure PIN for authorizing payments and transactions.", fontSize = 14.sp, color = Gray500)
    Spacer(Modifier.height(20.dp))
    OutlinedTextField(
        value = pin, onValueChange = onPin,
        label = { Text("Transaction PIN (min 4 digits)") },
        modifier = Modifier.fillMaxWidth(), singleLine = true,
        visualTransformation = PasswordVisualTransformation(),
        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
        colors = OutlinedTextFieldDefaults.colors(focusedBorderColor = KenyaGreen)
    )
    Spacer(Modifier.height(12.dp))
    OutlinedTextField(
        value = confirmPin, onValueChange = onConfirm,
        label = { Text("Confirm PIN") },
        modifier = Modifier.fillMaxWidth(), singleLine = true,
        visualTransformation = PasswordVisualTransformation(),
        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
        isError = confirmPin.isNotEmpty() && confirmPin != pin,
        supportingText = if (confirmPin.isNotEmpty() && confirmPin != pin) {{ Text("PINs do not match") }} else null,
        colors = OutlinedTextFieldDefaults.colors(focusedBorderColor = KenyaGreen)
    )
}

@Composable
private fun StepPrivacy(agreeTerms: Boolean, agreePrivacy: Boolean, onTerms: () -> Unit, onPrivacy: () -> Unit) {
    Text("Privacy & Terms", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = Gray900)
    Spacer(Modifier.height(16.dp))
    Card(
        modifier = Modifier.fillMaxWidth().clickable { onTerms() },
        shape = RoundedCornerShape(12.dp),
        border = if (agreeTerms) androidx.compose.foundation.BorderStroke(2.dp, KenyaGreen) else null,
        colors = CardDefaults.cardColors(containerColor = if (agreeTerms) KenyaGreenLight else Color.White),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    ) {
        Row(modifier = Modifier.padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
            Checkbox(checked = agreeTerms, onCheckedChange = { onTerms() }, colors = CheckboxDefaults.colors(checkedColor = KenyaGreen))
            Text("I agree to the Terms of Service", color = Gray900)
        }
    }
    Spacer(Modifier.height(8.dp))
    Card(
        modifier = Modifier.fillMaxWidth().clickable { onPrivacy() },
        shape = RoundedCornerShape(12.dp),
        border = if (agreePrivacy) androidx.compose.foundation.BorderStroke(2.dp, KenyaGreen) else null,
        colors = CardDefaults.cardColors(containerColor = if (agreePrivacy) KenyaGreenLight else Color.White),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    ) {
        Row(modifier = Modifier.padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
            Checkbox(checked = agreePrivacy, onCheckedChange = { onPrivacy() }, colors = CheckboxDefaults.colors(checkedColor = KenyaGreen))
            Text("I agree to the Privacy Policy", color = Gray900)
        }
    }
}

@Composable
private fun StepCompletion(onComplete: () -> Unit, isLoading: Boolean) {
    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.fillMaxWidth()) {
        Icon(Icons.Default.CheckCircle, null, tint = KenyaGreen, modifier = Modifier.size(80.dp))
        Spacer(Modifier.height(16.dp))
        Text("You're all set!", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = Gray900)
        Spacer(Modifier.height(8.dp))
        Text("Your profile is complete. You can now access all government services through e-Citizen.", fontSize = 14.sp, color = Gray500, lineHeight = 22.sp)
        Spacer(Modifier.height(24.dp))
        Button(
            onClick = onComplete,
            modifier = Modifier.fillMaxWidth().height(50.dp),
            shape = RoundedCornerShape(12.dp),
            colors = ButtonDefaults.buttonColors(containerColor = KenyaGreen),
            enabled = !isLoading
        ) {
            if (isLoading) CircularProgressIndicator(color = Color.White, modifier = Modifier.size(20.dp))
            else Text("Go to Dashboard", fontWeight = FontWeight.SemiBold)
        }
    }
}
