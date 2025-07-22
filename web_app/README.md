# 🌐 UltraEfficientLLM Web Application

Aplicación web profesional para entrenar y evaluar el UltraEfficientLLM usando FastAPI y React.

## 🚀 Características

### **Backend (FastAPI)**
- ✅ API RESTful completa
- ✅ Subida de archivos para entrenamiento
- ✅ Entrenamiento del modelo con parámetros configurables
- ✅ Generación de texto con análisis de patrones
- ✅ Monitoreo en tiempo real del estado del modelo
- ✅ Gestión de archivos subidos
- ✅ Documentación automática (Swagger/ReDoc)

### **Frontend (React + Vite)**
- ✅ Interfaz moderna y responsiva
- ✅ Dashboard con métricas en tiempo real
- ✅ Subida de archivos con drag & drop
- ✅ Configuración avanzada de entrenamiento
- ✅ Generación de texto con parámetros ajustables
- ✅ Análisis de patrones activos
- ✅ Notificaciones en tiempo real

## 📁 Estructura del Proyecto

```
web_app/
├── backend/                 # 🐍 Backend FastAPI
│   ├── main.py             # API principal
│   ├── requirements.txt    # Dependencias Python
│   └── uploads/            # Archivos subidos
├── frontend/               # ⚛️ Frontend React
│   ├── src/
│   │   ├── components/     # Componentes reutilizables
│   │   ├── pages/          # Páginas de la aplicación
│   │   ├── services/       # Servicios de API
│   │   └── types/          # Tipos TypeScript
│   ├── package.json        # Dependencias Node.js
│   ├── vite.config.ts      # Configuración Vite
│   └── tailwind.config.js  # Configuración Tailwind
└── README.md               # Este archivo
```

## 🛠️ Instalación y Configuración

### **1. Backend (FastAPI)**

```bash
cd web_app/backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python main.py
```

**El backend estará disponible en:** `http://localhost:8000`
**Documentación API:** `http://localhost:8000/api/docs`

### **2. Frontend (React)**

```bash
cd web_app/frontend

# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
npm run dev
```

**El frontend estará disponible en:** `http://localhost:5173`

## 🎯 Uso de la Aplicación

### **1. Dashboard**
- Vista general del estado del modelo
- Métricas en tiempo real
- Acceso rápido a todas las funciones

### **2. Entrenamiento**
- Subir archivos de texto (.txt, .md, .json, .csv)
- Configurar parámetros de entrenamiento
- Monitorear progreso en tiempo real
- Ver estadísticas del entrenamiento

### **3. Generación**
- Escribir prompts personalizados
- Ajustar temperatura y longitud
- Ver análisis de patrones activos
- Copiar resultados generados

### **4. Estado del Modelo**
- Métricas detalladas de rendimiento
- Información de memoria y patrones
- Reiniciar modelo si es necesario

## 🔧 Configuración Avanzada

### **Parámetros de Entrenamiento**
- **Máximo de Patrones**: 1,000 - 50,000 (default: 10,000)
- **Longitud Máxima de Patrón**: 3 - 15 (default: 8)
- **Frecuencia Mínima**: 1 - 10 (default: 1)

### **Parámetros de Generación**
- **Temperatura**: 0.1 - 2.0 (default: 0.7)
- **Longitud Máxima**: 5 - 50 tokens (default: 20)

## 📊 API Endpoints

### **Estado del Modelo**
- `GET /api/health` - Health check
- `GET /api/model/status` - Estado actual del modelo

### **Gestión de Archivos**
- `POST /api/upload` - Subir archivo
- `GET /api/files` - Listar archivos
- `DELETE /api/files/{filename}` - Eliminar archivo

### **Entrenamiento**
- `POST /api/train` - Entrenar modelo con archivos

### **Generación**
- `POST /api/generate` - Generar texto

### **Administración**
- `POST /api/reset` - Reiniciar modelo

## 🎨 Características de la UI

### **Diseño Responsivo**
- Adaptable a móviles, tablets y desktop
- Navegación intuitiva
- Feedback visual en tiempo real

### **Componentes Modernos**
- Drag & drop para subida de archivos
- Barras de progreso animadas
- Notificaciones toast
- Iconos de Lucide React

### **Tema Personalizado**
- Paleta de colores profesional
- Tipografía Inter
- Animaciones suaves
- Estados de hover y focus

## 🔍 Monitoreo y Análisis

### **Métricas en Tiempo Real**
- Patrones almacenados
- Uso de memoria
- Sparsity del modelo
- Estado de entrenamiento

### **Análisis de Patrones**
- Patrones activos por prompt
- Scores de relevancia
- Análisis de eficiencia

## 🚀 Despliegue

### **Desarrollo**
```bash
# Terminal 1 - Backend
cd web_app/backend
python main.py

# Terminal 2 - Frontend
cd web_app/frontend
npm run dev
```

### **Producción**
```bash
# Build del frontend
cd web_app/frontend
npm run build

# El backend servirá los archivos estáticos
```

## 🔧 Personalización

### **Configuración del Backend**
- Modificar `main.py` para cambiar endpoints
- Ajustar parámetros del modelo en `UltraEfficientLLM`
- Configurar CORS para diferentes dominios

### **Configuración del Frontend**
- Modificar `tailwind.config.js` para cambiar el tema
- Ajustar componentes en `src/components/`
- Personalizar páginas en `src/pages/`

## 📝 Notas Técnicas

### **Backend**
- FastAPI con async/await
- Manejo de archivos multipart
- CORS configurado para desarrollo
- Validación de tipos con Pydantic

### **Frontend**
- React 18 con hooks
- TypeScript para type safety
- Vite para desarrollo rápido
- Tailwind CSS para estilos

### **Comunicación**
- API RESTful
- FormData para subida de archivos
- JSON para respuestas
- WebSocket para actualizaciones en tiempo real (futuro)

## 🎉 ¡Listo para Usar!

La aplicación web está completamente funcional y lista para entrenar y evaluar el UltraEfficientLLM de forma profesional.

**¡Disfruta explorando las capacidades revolucionarias del modelo ultra-eficiente!** 🚀✨ 