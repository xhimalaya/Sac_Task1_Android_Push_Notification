<!-- src/surveydataupload/SurveyForm.vue -->
<template>
  <div class="survey-container">
    <h2>Survey Data Upload</h2>

    <div class="status">
      Status: 
      <span :class="{ online: isOnline && isApiReachable, offline: !(isOnline && isApiReachable) }">
        {{ isOnline && isApiReachable ? '🟢 Online' : '🔴 Offline / API Unreachable' }}
      </span>
    </div>

    <form @submit.prevent>
      <div class="field">
        <label>Name</label>
        <input v-model="form.name" type="text" required placeholder="Enter name" />
      </div>

      <div class="field">
        <label>Age</label>
        <input v-model.number="form.age" type="number" min="1" required placeholder="Enter age" />
      </div>

      <div class="field">
        <label>Location</label>
        <button type="button" @click="getLocation" :disabled="gettingLocation" class="location-btn">
          {{ location ? 'update Location' : ' Detect Location' }}
        </button>
        <div v-if="location" class="location-display">
          Lat: {{ location.lat.toFixed(4) }}, Lon: {{ location.lon.toFixed(4) }}
        </div>
      </div>

      <!-- Camera Section -->
      <div class="field photo-field">
        <label>Photo (Camera)</label>

        <!-- Live Camera View -->
        <div class="camera-container" v-if="cameraActive">
          <video ref="video" autoplay playsinline class="camera-video"></video>
          <canvas ref="canvas" class="hidden-canvas"></canvas>

          <div class="camera-controls">
            <button type="button" @click="switchCamera" class="switch-btn">↻ Switch Camera</button>
            <button type="button" @click="capturePhoto" class="capture-btn">📸 Capture</button>
            <button type="button" @click="stopCamera" class="cancel-btn">Cancel</button>
          </div>
        </div>
        <div v-else-if="previewUrl" class="preview">
          <img :src="previewUrl" alt="Captured photo" class="preview-img" />
          <div class="preview-actions">
            <button type="button" @click="retakePhoto" class="retake-btn">Retake</button>
            <button type="button" @click="confirmPhoto" class="confirm-btn">Use Photo</button>
          </div>
        </div>

        <!-- Start Camera Button -->
        <button 
          v-else
          type="button"
          @click="startCamera"
          class="open-camera-btn"
        >
          📷 Open Camera
        </button>

        <p v-if="cameraError" class="camera-error">{{ cameraError }}</p>
      </div>

      <div class="buttons">
        <button type="button" @click="saveToPending" :disabled="!isFormValid" class="save-btn">
          💾 Save to Pending
        </button>

        <button type="button" @click="submitCurrent" 
                :disabled="!isFormValid || !isOnline || !isApiReachable"
                class="submit-single-btn">
          🚀 Submit Now (Single)
        </button>

        <button type="button" @click="submitAllPending" 
                :disabled="pendingCount === 0 || !isOnline || !isApiReachable"
                class="submit-bulk-btn">
          📤 Submit All Pending ({{ pendingCount }})
        </button>
      </div>
    </form>

    <div v-if="pendingCount > 0" class="pending-section">
      <h3>Pending Submissions ({{ pendingCount }})</h3>
      <ul class="pending-list">
        <li v-for="item in pendingSurveys" :key="item.id">
          {{ item.name }} • Age {{ item.age }} • {{ new Date(item.timestamp).toLocaleString() }}
          <button @click="deletePending(item.id)" class="delete-btn">×</button>
        </li>
      </ul>
    </div>

    <p v-if="message" :class="['message', messageType]">{{ message }}</p>
  </div>
</template>

<script>
import { loadPendingSurveys, savePendingSurveys, addPendingSurvey, clearPendingSurveys, removePendingSurvey } from './surveyStorage.js';
import { checkApiReachable, submitSingle, submitBulk } from './apiClient.js';

export default {
  data() {
    return {
      form: { name: '', age: '', location: null },
      previewUrl: null,
      imageFile: null,
      imageBase64: null,
      pendingSurveys: [],
      isOnline: navigator.onLine,
      isApiReachable: false,
      gettingLocation: false,
      message: '',
      messageType: '',

      // Camera
      cameraActive: false,
      cameraStream: null,
      cameraError: '',
      currentFacingMode: 'environment',
    };
  },
  computed: {
    pendingCount() { return this.pendingSurveys.length; },
    location() { return this.form.location; },
    isFormValid() {
      return this.form.name.trim() && 
             this.form.age > 0 && 
             this.form.location && 
             this.imageFile;
    }
  },
  async mounted() {
    this.pendingSurveys = loadPendingSurveys();
    window.addEventListener('online', this.updateConnectivity);
    window.addEventListener('offline', this.updateConnectivity);
    await this.updateConnectivity();
  },
  beforeUnmount() {
    this.stopCamera();
    window.removeEventListener('online', this.updateConnectivity);
    window.removeEventListener('offline', this.updateConnectivity);
  },
  methods: {
    async updateConnectivity() {
      this.isOnline = navigator.onLine;
      if (this.isOnline) {
        this.isApiReachable = await checkApiReachable();
      } else {
        this.isApiReachable = false;
      }
    },

    async getLocation() {
      if (!navigator.geolocation) return alert('Geolocation not supported');
      this.gettingLocation = true;
      try {
        const pos = await new Promise((resolve, reject) => {
          navigator.geolocation.getCurrentPosition(resolve, reject, { 
            enableHighAccuracy: true, 
            timeout: 15000 
          });
        });
        this.form.location = {
          lat: pos.coords.latitude,
          lon: pos.coords.longitude
        };
      } catch (err) {
        alert('Could not get location: ' + err.message);
      }
      this.gettingLocation = false;
    },

    async startCamera() {
      this.cameraError = '';
      try {
        if (this.cameraStream) this.stopCamera();

        const constraints = {
          video: {
            facingMode: this.currentFacingMode,
            width: { ideal: 1280 },
            height: { ideal: 720 }
          }
        };

        this.cameraStream = await navigator.mediaDevices.getUserMedia(constraints);
        this.$refs.video.srcObject = this.cameraStream;
        this.cameraActive = true;

        await new Promise(resolve => {
          this.$refs.video.onloadedmetadata = resolve;
        });
      } catch (err) {
        this.cameraError = 'Camera access failed: ' + err.message;
        console.error('Camera error:', err);
      }
    },

    stopCamera() {
      if (this.cameraStream) {
        this.cameraStream.getTracks().forEach(track => track.stop());
        this.cameraStream = null;
      }
      this.cameraActive = false;
    },

    async switchCamera() {
      this.currentFacingMode = this.currentFacingMode === 'environment' ? 'user' : 'environment';
      await this.startCamera();
    },

    capturePhoto() {
      const video = this.$refs.video;
      const canvas = this.$refs.canvas;
      if (!video || !canvas) return;

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

      const dataUrl = canvas.toDataURL('image/jpeg', 0.85);
      this.previewUrl = dataUrl;
      this.imageBase64 = dataUrl;

      fetch(dataUrl)
        .then(res => res.blob())
        .then(blob => {
          this.imageFile = new File([blob], `capture_${Date.now()}.jpg`, { type: 'image/jpeg' });
        });

      this.stopCamera();
    },

    retakePhoto() {
      this.previewUrl = null;
      this.imageBase64 = null;
      this.imageFile = null;
      this.startCamera();
    },

    confirmPhoto() {
      this.cameraActive = true;
    },

    saveToPending() {
      if (!this.isFormValid) return;
      addPendingSurvey({
        name: this.form.name.trim(),
        age: this.form.age,
        location: this.form.location,
        imageBase64: this.imageBase64,
        client_id: crypto.randomUUID()
      });
      this.pendingSurveys = loadPendingSurveys();
      this.resetForm();
      this.showMessage('Saved to pending list', 'success');
    },

    async submitCurrent() {
      if (!this.isFormValid) return;
      try {
        await submitSingle({
          name: this.form.name.trim(),
          age: this.form.age,
          location: this.form.location
        }, this.imageFile);
        this.showMessage('Single entry submitted successfully', 'success');
        this.resetForm();
      } catch (err) {
        this.showMessage('Submit failed: ' + err.message, 'error');
      }
    },

    async submitAllPending() {
      if (this.pendingCount === 0) return;
      try {
        await submitBulk(this.pendingSurveys);
        clearPendingSurveys();
        this.pendingSurveys = [];
        this.showMessage('All pending entries submitted!', 'success');
      } catch (err) {
        this.showMessage('Bulk submit failed: ' + err.message, 'error');
      }
    },

    deletePending(id) {
      removePendingSurvey(id);
      this.pendingSurveys = loadPendingSurveys();
    },

    resetForm() {
      this.form = { name: '', age: '', location: null };
      this.previewUrl = null;
      this.imageFile = null;
      this.imageBase64 = null;
      this.stopCamera();
    },

    showMessage(text, type) {
      this.message = text;
      this.messageType = type;
      setTimeout(() => { this.message = ''; }, 5000);
    }
  }
};
</script>

<style scoped>
.survey-container { padding: 1rem; max-width: 600px; margin: 0 auto; font-family: system-ui, sans-serif; }
.field { margin-bottom: 1.5rem; }
label { display: block; margin-bottom: 0.5rem; font-weight: 600; }

input, button { width: 100%; padding: 0.75rem; font-size: 1rem; }

.camera-container { position: relative; margin: 1rem 0; background: #000; border-radius: 12px; overflow: hidden; }
.camera-video { width: 100%; display: block; }
.camera-controls { position: absolute; bottom: 20px; left: 0; right: 0; display: flex; gap: 12px; justify-content: center; }
.capture-btn { background: #ff3b30; color: white; border: none; width: 70px; height: 70px; border-radius: 50%; font-size: 28px; }
.switch-btn, .cancel-btn { padding: 10px 16px; border-radius: 8px; font-size: 0.9rem; }

.preview { margin: 1rem 0; text-align: center; }
.preview-img { max-width: 100%; max-height: 300px; border-radius: 12px; border: 3px solid #0d6efd; }
.preview-actions { margin-top: 1rem; display: flex; gap: 1rem; }

.open-camera-btn { background: #0d6efd; color: white; font-weight: bold; padding: 1rem; border-radius: 8px; }

.buttons { display: flex; flex-direction: column; gap: 0.75rem; margin-top: 1.5rem; }
button:disabled { opacity: 0.5; cursor: not-allowed; }

.pending-section h3 { margin: 1.5rem 0 0.5rem; }
.pending-list { padding: 0; list-style: none; }
.pending-list li { padding: 0.75rem; background: #f8f9fa; margin-bottom: 0.5rem; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; }

.status { font-weight: bold; margin-bottom: 1rem; }
.online { color: #28a745; }
.offline { color: #dc3545; }
.camera-error { color: #dc3545; margin-top: 0.5rem; }
.message.success { color: #28a745; }
.message.error { color: #dc3545; }
</style>