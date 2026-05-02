package com.ecitizen.kenya.ui.wallet

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.ecitizen.kenya.data.api.models.WalletTransactionDto
import com.ecitizen.kenya.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun WalletScreen(
    onNavigateBack: () -> Unit,
    viewModel: WalletViewModel = viewModel()
) {
    val state by viewModel.state.collectAsState()

    LaunchedEffect(state.topUpMessage) {
        state.topUpMessage?.let { viewModel.clearTopUpMessage() }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("My Wallet", fontWeight = FontWeight.Bold) },
                navigationIcon = { IconButton(onClick = onNavigateBack) { Icon(Icons.Default.ArrowBack, "Back", tint = Color.White) } },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = KenyaGreen, titleContentColor = Color.White)
            )
        }
    ) { padding ->
        if (state.isLoading) {
            Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                CircularProgressIndicator(color = KenyaGreen)
            }
        } else if (state.error != null && state.wallet == null) {
            Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text(state.error!!, color = ErrorRed, fontSize = 14.sp)
                    Spacer(Modifier.height(12.dp))
                    Button(onClick = { viewModel.loadWallet() }, colors = ButtonDefaults.buttonColors(containerColor = KenyaGreen)) {
                        Text("Retry")
                    }
                }
            }
        } else {
            LazyColumn(
                modifier = Modifier.padding(padding),
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                // Balance Hero Card
                item {
                    Card(
                        shape = RoundedCornerShape(20.dp),
                        colors = CardDefaults.cardColors(containerColor = Color.Transparent),
                        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
                    ) {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .background(Brush.linearGradient(listOf(KenyaGreen, KenyaGreenDark)), RoundedCornerShape(20.dp))
                                .padding(24.dp)
                        ) {
                            Column {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(Icons.Default.AccountBalanceWallet, null, tint = Color.White.copy(0.7f), modifier = Modifier.size(20.dp))
                                    Spacer(Modifier.width(8.dp))
                                    Text("Available Balance", color = Color.White.copy(alpha = 0.85f), fontSize = 14.sp)
                                }
                                Spacer(Modifier.height(12.dp))
                                Text(
                                    "KES %,d".format(state.wallet?.balance?.toLong() ?: 0),
                                    color = Color.White,
                                    fontSize = 32.sp,
                                    fontWeight = FontWeight.Bold
                                )
                                if (state.wallet != null) {
                                    Spacer(Modifier.height(4.dp))
                                    Text("Wallet ID: ${state.wallet!!.walletId}", color = Color.White.copy(0.6f), fontSize = 12.sp)
                                }
                            }
                        }
                    }
                }

                // Top Up Section
                item {
                    Card(
                        shape = RoundedCornerShape(16.dp),
                        colors = CardDefaults.cardColors(containerColor = Color.White),
                        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            Text("Top Up Wallet", fontWeight = FontWeight.Bold, fontSize = 16.sp, color = Gray900)
                            Spacer(Modifier.height(12.dp))
                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.spacedBy(12.dp)
                            ) {
                                OutlinedTextField(
                                    value = state.topUpAmount,
                                    onValueChange = { viewModel.setTopUpAmount(it) },
                                    label = { Text("Amount (KES)") },
                                    modifier = Modifier.weight(1f),
                                    singleLine = true,
                                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                                    colors = OutlinedTextFieldDefaults.colors(focusedBorderColor = KenyaGreen)
                                )
                                Button(
                                    onClick = { viewModel.topUp() },
                                    modifier = Modifier.height(56.dp),
                                    enabled = (state.topUpAmount.toDoubleOrNull() ?: 0.0) > 0,
                                    shape = RoundedCornerShape(12.dp),
                                    colors = ButtonDefaults.buttonColors(containerColor = KenyaGreen)
                                ) {
                                    Text("Top Up")
                                }
                            }
                        }
                    }
                }

                // Quick actions
                item {
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                        QuickActionCard("Send", Icons.Default.Send, KenyaGreen, Modifier.weight(1f))
                        QuickActionCard("Request", Icons.Default.CallReceived, InfoBlue, Modifier.weight(1f))
                        QuickActionCard("Pay Bill", Icons.Default.Receipt, KenyaRed, Modifier.weight(1f))
                    }
                }

                // Transaction History
                item {
                    Text("Recent Transactions", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Gray900)
                }

                if (state.recentTransactions.isEmpty()) {
                    item {
                        Card(
                            shape = RoundedCornerShape(12.dp),
                            colors = CardDefaults.cardColors(containerColor = Color.White),
                            elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
                        ) {
                            Column(modifier = Modifier.padding(24.dp).fillMaxWidth(), horizontalAlignment = Alignment.CenterHorizontally) {
                                Icon(Icons.Default.ReceiptLong, null, tint = Gray400, modifier = Modifier.size(40.dp))
                                Spacer(Modifier.height(8.dp))
                                Text("No transactions yet", color = Gray500, fontSize = 14.sp)
                            }
                        }
                    }
                } else {
                    items(state.recentTransactions) { tx ->
                        TransactionCard(tx)
                    }
                }
                item { Spacer(Modifier.height(16.dp)) }
            }
        }
    }
}

@Composable
private fun QuickActionCard(label: String, icon: androidx.compose.ui.graphics.vector.ImageVector, color: Color, modifier: Modifier) {
    Card(
        modifier = modifier,
        shape = RoundedCornerShape(14.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp).fillMaxWidth(), horizontalAlignment = Alignment.CenterHorizontally) {
            Icon(icon, null, tint = color, modifier = Modifier.size(24.dp))
            Spacer(Modifier.height(6.dp))
            Text(label, fontSize = 12.sp, color = Gray700, fontWeight = FontWeight.Medium)
        }
    }
}

@Composable
private fun TransactionCard(tx: WalletTransactionDto) {
    val isDebit = tx.transactionType in listOf("withdrawal", "payment", "transfer")
    val icon = when (tx.transactionType) {
        "deposit" -> Icons.Default.ArrowDownward
        "withdrawal" -> Icons.Default.ArrowUpward
        "payment" -> Icons.Default.ShoppingCart
        "refund" -> Icons.Default.Undo
        else -> Icons.Default.SwapHoriz
    }
    val color = if (isDebit) ErrorRed else SuccessGreen

    Card(
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    ) {
        Row(modifier = Modifier.padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
            Surface(shape = RoundedCornerShape(10.dp), color = color.copy(alpha = 0.1f)) {
                Icon(icon, null, tint = color, modifier = Modifier.padding(8.dp).size(20.dp))
            }
            Spacer(Modifier.width(12.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(tx.transactionType.replaceFirstChar { it.uppercase() }, fontWeight = FontWeight.Medium, color = Gray900, fontSize = 14.sp)
                Text(tx.reference, fontSize = 11.sp, color = Gray500)
            }
            Column(horizontalAlignment = Alignment.End) {
                val prefix = if (isDebit) "-" else "+"
                Text("$prefix KES %,d".format(tx.amount.toLong()), fontWeight = FontWeight.Medium, color = color, fontSize = 14.sp)
                Text("KES %,d".format(tx.balanceAfter.toLong()), fontSize = 11.sp, color = Gray400)
            }
        }
    }
}
