import streamlit as base_st
from datetime import datetime, timedelta
import streamlit.components.v1 as components
import time


base_st.set_page_config(page_title="Inspector Vial", page_icon="🚗", layout="centered")


base_st.title("🛡️ Inspector Vial")
base_st.subheader("Unidad de Monitoreo Urbano - Lima, Perú")
base_st.markdown("---")

hora_lima = datetime.now() - timedelta(hours=5)
hora_actual = hora_lima.strftime("%d/%m/%Y — %H:%M:%S")
base_st.markdown(f"### ⏱️ **Fecha y Hora de Captura:** `{hora_actual}`")


distritos_lima = [
    "Lima Cercado", "Breña", "Jesús María", "La Victoria", "Lince", "Magdalena del Mar", 
    "Miraflores", "Pueblo Libre", "San Borja", "San Isidro", "San Luis", "San Miguel", 
    "Santiago de Surco", "Surquillo", "Barranco", "Chorrillos", "Ancón", "Carabayllo", 
    "Comas", "Independencia", "Los Olivos", "Puente Piedra", "San Martín de Porres", 
    "Santa Rosa", "Ate", "Chaclacayo", "Cieneguilla", "El Agustino", "La Molina", 
    "Lurigancho-Chosica", "San Juan de Lurigancho", "Santa Anita", "Lurín", "Pachacámac", 
    "Pucusana", "Punta Hermosa", "Punta Negra", "San Bartolo", "San Juan de Miraflores", 
    "Santa María del Mar", "Villa El Salvador", "Villa María del Triunfo"
]
distrito = base_st.selectbox("📍 **Jurisdicción Vial (Seleccione el Distrito de Lima):**", distritos_lima)
base_st.write(f"**Ubicación registrada para el informe:** {distrito}, Lima, Perú.")
base_st.markdown("---")



URL_TEACHABLE_MACHINE = "https://teachablemachine.withgoogle.com/models/pnGtXoxsJ/"


html_code = f"""
<div style="text-align: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #1e1e1e; color: white; padding: 25px; border-radius: 10px; overflow: visible;">
    
    <input type="file" id="imageSelector" accept="image/*" onchange="processImage(event)" style="display: none;" />
    <button type="button" onclick="document.getElementById('imageSelector').click()" style="background-color: #0066cc; color: white; border: none; padding: 14px 28px; font-size: 16px; border-radius: 5px; cursor: pointer; margin-bottom: 20px; font-weight: bold; width: 100%; max-width: 450px; text-transform: uppercase;">
        📁 Seleccionar o Arrastrar Imagen Vial
    </button>
    
    <div style="margin-top: 15px; display: flex; justify-content: center; margin-bottom: 20px;">
        <img id="preview" style="max-height: 320px; max-width: 100%; border-radius: 8px; display: none; box-shadow: 0px 4px 10px rgba(0,0,0,0.5);" />
    </div>
    
    <div id="veredicto-container" style="margin-top: 25px; text-align: left; max-width: 600px; margin-left: auto; margin-right: auto; overflow: visible;"></div>
</div>

<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest/dist/tf.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@teachablemachine/image@latest/dist/teachablemachine-image.min.js"></script>
<script type="text/javascript">
    const URL = "{URL_TEACHABLE_MACHINE}";
    let model, maxPredictions;

    // Cargar el modelo de forma asíncrona al iniciar el componente
    async function loadModel() {{
        const modelURL = URL + "model.json";
        const metadataURL = URL + "metadata.json";
        model = await tmImage.load(modelURL, metadataURL);
        maxPredictions = model.getTotalClasses();
    }}
    loadModel();

    function processImage(event) {{
        const reader = new FileReader();
        reader.onload = function() {{
            const imgElement = document.getElementById('preview');
            imgElement.src = reader.result;
            imgElement.style.display = "block";
            
            // Esperar un instante a que cargue el elemento visual para predecir
            imgElement.onload = async function() {{
                await predict(imgElement);
            }}
        }}
        reader.readAsDataURL(event.target.files[0]);
    }}

    async function predict(imgElement) {{
        if (!model) return;
        
        const prediction = await model.predict(imgElement);
        
        let maxProb = 0;
        let claseGanadora = "";
        
        // Evaluar la predicción con mayor porcentaje
        for (let i = 0; i < maxPredictions; i++) {{
            if (prediction[i].probability > maxProb) {{
                maxProb = prediction[i].probability;
                claseGanadora = prediction[i].className;
            }}
        }}

        let porcentaje = (maxProb * 100).toFixed(0);
        const veredictoContainer = document.getElementById("veredicto-container");
        
        let htmlMensaje = "";
        
        // Renderizado del mensaje correspondiente según la escala ganadora de la IA
        if (claseGanadora.includes("1")) {{
            htmlMensaje = `<div style='background-color: #e2f0d9; color: #385723; border-left: 6px solid #70ad47; padding: 18px; border-radius: 5px; font-size: 15px;'>
                <strong>🟢 ESTADO: ÓPTIMO (Nivel de daño 1 — Certeza: ${{porcentaje}}%)</strong><br><br>
                El pavimento se encuentra en excelentes condiciones. No requiere intervenciones correctivas inmediatas en la jurisdicción de {distrito}.</div>`;
        }} 
        else if (claseGanadora.includes("2")) {{
            htmlMensaje = `<div style='background-color: #e2f0d9; color: #385723; border-left: 6px solid #70ad47; padding: 18px; border-radius: 5px; font-size: 15px;'>
                <strong>🟡 ESTADO: LEVE (Nivel de daño 2 — Certeza: ${{porcentaje}}%)</strong><br><br>
                Se observan desgastes menores o fisuras iniciales. Se recomienda programar mantenimiento preventivo por la municipalidad distrital de {distrito}.</div>`;
        }} 
        else if (claseGanadora.includes("3")) {{
            htmlMensaje = `<div style='background-color: #fff3cd; color: #856404; border-left: 6px solid #ffc107; padding: 18px; border-radius: 5px; font-size: 15px;'>
                <strong>🟠 ESTADO: MODERADO (Nivel de daño 3 — Certeza: ${{porcentaje}}%)</strong><br><br>
                Presencia visible de grietas extendidas o pequeños baches en {distrito}. Requiere mantenimiento correctivo programado (bacheo superficial).</div>`;
        }} 
        else if (claseGanadora.includes("4")) {{
            htmlMensaje = `<div style='background-color: #f8d7da; color: #721c24; border-left: 6px solid #dc3545; padding: 18px; border-radius: 5px; font-size: 15px;'>
                <strong>🔴 ESTADO: SEVERO (Nivel de daño 4 — Certeza: ${{porcentaje}}%)</strong><br><br>
                Deterioro avanzado de la calzada con baches profundos que ponen en riesgo el tránsito de {distrito}. Requiere reparación prioritaria municipal.</div>`;
        }} 
        else if (claseGanadora.includes("5")) {{
            htmlMensaje = `<div style='background-color: #f8d7da; color: #721c24; border-left: 6px solid #721c24; padding: 18px; border-radius: 5px; font-size: 15px;'>
                <strong>🚨 ALERTA CRÍTICA RELEVADA: DAÑO MÁXIMO (Nivel de daño 5 — Certeza: ${{porcentaje}}%)</strong><br><br>
                Estructura vial severamente colapsada en el distrito de {distrito} que representa un peligro inminente para la seguridad ciudadana.<br><br>
                <strong>Acción Automatizada del Sistema:</strong> Se ha generado un expediente técnico con fecha {hora_actual} y se procederá a derivar el informe de manera inmediata al <strong>Ministerio de Transportes y Comunicaciones (MTC)</strong> para su intervención de emergencia.</div>`;
        }}
        
        veredictoContainer.innerHTML = htmlMensaje;
    }}
</script>
"""

components.html(html_code, height=750)
