import re

with open('app/src/main/java/com/example/ui/theme/Color.kt', 'w') as f:
    f.write("""package com.example.ui.theme

import androidx.compose.ui.graphics.Color

val PrimaryBlue = Color(0xFF9EA8FF)
val OnPrimaryBlue = Color(0xFF141940)
val BackgroundDark = Color(0xFF111114)
val SurfaceDark = Color(0xFF1B1B1F)
val SurfaceVariantDark = Color(0xFF2B2B30)
val OnBackgroundDark = Color(0xFFE3E2E6)
val OnSurfaceVariantDark = Color(0xFFC4C6D0)
val ErrorRed = Color(0xFFFF5449)
val SuccessGreen = Color(0xFF4CAF50)
""")

with open('app/src/main/java/com/example/ui/theme/Theme.kt', 'w') as f:
    f.write("""package com.example.ui.theme

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
""")
