with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    text = f.read()
    
# Find the end of Custom Chart box
import re
target = """// Custom Chart
                        Box(modifier = Modifier.fillMaxWidth().height(150.dp)) {
                            ChartCurve(color = MaterialTheme.colorScheme.primary, dataPoints = weeklySales)
                        }"""
start_idx = text.find(target)

if start_idx != -1:
    end_idx = text.find("// Top Performing Items")
    
    # We want to replace from start_idx to end_idx with correct brackets
    replacement = """// Custom Chart
                        Box(modifier = Modifier.fillMaxWidth().height(150.dp)) {
                            ChartCurve(color = MaterialTheme.colorScheme.primary, dataPoints = weeklySales)
                        }
                        
                        val daysList = mutableListOf<String>()
                        val sdf = SimpleDateFormat("EEE", Locale.US)
                        for (i in 6 downTo 0) {
                            daysList.add(sdf.format(Date(todayMillis - (i * 86400000L))))
                        }
                        Row(
                            modifier = Modifier.fillMaxWidth().padding(top = 8.dp),
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            daysList.forEach {
                                Text(it, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                        }
                    }
                }
            }
            
            """
    text = text[:start_idx] + replacement + text[end_idx:]

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(text)

