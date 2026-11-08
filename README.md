# AEGISAI NEXUS — Flutter client

Mobile client for the existing AegisAI Nexus FastAPI backend (`/api/v1`). It does **not** add a new backend.

## Status — read this first
- **Not compiled or run.** It was written without a Flutter SDK available. Expect a few small compile fixes on first `flutter analyze`.
- **No OpenAPI spec or PDF was available**, so request/response field names are tolerant guesses. Before trusting live mode, compare each call in `lib/services/api_service.dart` with your running `/openapi.json` (login form-vs-JSON, incident create JSON-vs-multipart, field names).
- `android/` and `ios/` are not included; `flutter create` generates them.

## Run
```bash
flutter create . --platforms=android,ios --org com.example.aegisai   # one time; keeps lib/ and pubspec.yaml
flutter pub get
flutter analyze && flutter test
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000/api/v1           # Android emulator -> host
flutter run --dart-define=API_BASE_URL=https://YOUR-HOST/api/v1 --dart-define=LOGIN_AS_FORM=false
```
No backend? Sign in with a **Demo · ROLE** button. Everything is then DEMO data, labelled.

## Platform setup after `flutter create`
Android `android/app/src/main/AndroidManifest.xml` (inside `<manifest>`):
```xml
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION"/>
<uses-permission android:name="android.permission.CAMERA"/>
<uses-permission android:name="android.permission.POST_NOTIFICATIONS"/>
<uses-permission android:name="android.permission.VIBRATE"/>
```
For plain-HTTP dev only, add `android:usesCleartextTraffic="true"` to `<application>`. Remove it for release; use HTTPS.
`flutter_secure_storage` needs `minSdkVersion 23`; set it in `android/app/build.gradle`.

iOS `ios/Runner/Info.plist`: `NSLocationWhenInUseUsageDescription`, `NSCameraUsageDescription`, `NSPhotoLibraryUsageDescription`.

`flutter_local_notifications` is pinned to ^17; v18+ changed `show()`/`initialize()` signatures.

## Data provenance
Every API-driven screen shows a badge: **LIVE**, **DEMO**, **MOCK**, **SIMULATION**.
- Reads that fail fall back to DEMO with the text "Live service unavailable — displaying demo data."
- Writes (report, status change, deploy, broadcast) never fall back; a failed live write shows an error.
- Simulation is always SIMULATION, whether the backend or the on-device demo model computed it.

## Endpoint map (client side)
| Feature | Call | State |
|---|---|---|
| Login / register / me | POST `/auth/login`, POST `/auth/register`, GET `/auth/me` | wired |
| Alerts | GET/POST `/alerts` | wired |
| Incidents | GET/POST `/incidents`, PATCH `/incidents/{id}/status` | wired |
| Shelters / hospitals | GET `/shelters`, GET `/shelters/hospitals` | wired |
| Resources | GET `/resources`, PATCH `/resources/{id}/deploy` | wired (POST create has no UI) |
| Prediction | POST `/predictions/run`, GET `/predictions/history` | wired |
| Damage | POST `/damage/analyze` | wired |
| Evacuation | POST `/evacuation/route` | wired |
| Simulation / what-if | POST `/simulation/run`, `/simulation/what-if/compare` | wired, local fallback |
| Analytics / users / audit / settings | GET `/analytics/summary`, `/users`, `/audit`, `/settings` | wired |
| AI assistant | none in the API map | MOCK scripted replies |

## Not implemented yet
Firebase Auth and FCM remote push (need your Firebase project files), email-verification and phone-verification screens, emergency-profile setup, historical records screen, share action on alerts, multi-language strings, jurisdiction filtering (left to the server), map markers for incidents/resources (models carry no coordinates), alert siren sound beyond the notification channel, user create/edit/disable UI, and a custom in-app critical-alert modal.
