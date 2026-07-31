package com.example.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable

private val AppColorScheme = darkColorScheme(
    primary = PrimaryBlue,
    onPrimary = OnPrimaryBlue,
    primaryContainer = PrimaryBlue,
    onPrimaryContainer = OnPrimaryBlue,
    background = BackgroundDark,
    onBackground = OnBackgroundDark,
    surface = SurfaceDark,
    onSurface = OnBackgroundDark,
    surfaceVariant = SurfaceVariantDark,
    onSurfaceVariant = OnSurfaceVariantDark,
    error = ErrorRed,
    secondaryContainer = SurfaceVariantDark,
    onSecondaryContainer = PrimaryBlue
)

@Composable
fun MyApplicationTheme(
    darkTheme: Boolean = true, // Force dark theme to match design
    dynamicColor: Boolean = false, // Disable dynamic to keep brand colors
    content: @Composable () -> Unit,
) {
    MaterialTheme(
        colorScheme = AppColorScheme,
        typography = Typography,
        content = content
    )
}
