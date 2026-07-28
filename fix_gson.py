with open('app/build.gradle.kts', 'r') as f:
    content = f.read()

content = content.replace('implementation(libs.moshi.kotlin)', 'implementation(libs.moshi.kotlin)\n  implementation("com.google.code.gson:gson:2.10.1")')

with open('app/build.gradle.kts', 'w') as f:
    f.write(content)
