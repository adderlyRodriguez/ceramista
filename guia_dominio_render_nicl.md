# Guía: Asignar dominio de nic.cl a una app en Render.com

## Requisitos previos
- App publicada en Render.com (ej: `miapp.onrender.com`)
- Dominio comprado en nic.cl (ej: `midominio.cl`)
- Cuenta en Cloudflare (gratis en cloudflare.com)

> **¿Por qué Cloudflare?** nic.cl no tiene editor de registros DNS propios. Cloudflare actúa como intermediario gratuito y permite agregar los registros CNAME/A que Render necesita.

---

## Paso 1 — Obtener los datos DNS de Render

1. Entra a [render.com](https://render.com) → tu servicio
2. Ve a **Settings** → **Custom Domains** → **Add Custom Domain**
3. Escribe tu dominio (ej: `midominio.cl`) y confirma
4. Render mostrará los registros DNS necesarios. Anota:
   - IP para registro A: `216.24.57.1`
   - Target para CNAME: `miapp.onrender.com`

---

## Paso 2 — Agregar el dominio en Cloudflare

1. Entra a [cloudflare.com](https://cloudflare.com) → **Add a domain**
2. Escribe `midominio.cl` y selecciona el plan **Free**
3. Cloudflare escaneará los registros DNS actuales — **elimina todos los que encuentre**
4. Agrega los registros correctos con **Add record**:

| Type  | Name  | Value                  | Proxy  |
|-------|-------|------------------------|--------|
| `A`   | `@`   | `216.24.57.1`          | On (nube naranja) |
| `CNAME` | `www` | `miapp.onrender.com` | On (nube naranja) |

5. Haz clic en **Continue to activation**
6. Cloudflare te asignará dos nameservers, por ejemplo:
   - `bradley.ns.cloudflare.com`
   - `meadow.ns.cloudflare.com`

---

## Paso 3 — Cambiar nameservers en nic.cl

1. Entra a [nic.cl](https://www.nic.cl) → administrar `midominio.cl`
2. Ve a **Configuración Técnica** → **Servidores DNS**
3. **Elimina** los nameservers actuales de nic.cl
4. Agrega los dos nameservers de Cloudflare del paso anterior
5. Haz clic en **Actualizar datos de dominio**

---

## Paso 4 — Esperar propagación

- Cloudflare verificará los nameservers automáticamente
- Tiempo estimado: **30 minutos a 2 horas**
- Recibirás un email de confirmación cuando el dominio esté activo en Cloudflare

---

## Paso 5 — Verificar en Render

1. Vuelve a Render.com → **Settings** → **Custom Domains**
2. Haz clic en **Retry Verification**
3. Render activará el certificado SSL automáticamente

---

## Resultado final

| URL | Estado |
|-----|--------|
| `midominio.cl` | Activo con SSL |
| `www.midominio.cl` | Activo con SSL |
| `miapp.onrender.com` | Sigue funcionando |

---

## Solución de problemas

| Problema | Causa probable | Solución |
|----------|---------------|----------|
| "Nombre de host NS inválido" en nic.cl | Intentaste poner `miapp.onrender.com` como nameserver | Usa solo los nameservers de Cloudflare |
| Render no verifica el dominio | DNS aún propagando | Espera y usa **Retry Verification** |
| Cloudflare detecta registros viejos | nic.cl tenía redirección web configurada | Elimínalos antes de agregar los nuevos |
