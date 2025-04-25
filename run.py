from app import create_app

# Crear la instancia de la aplicación
app = create_app()

if __name__ == '__main__':
    # Ejecutar la aplicación en modo de desarrollo (debug) solo cuando sea necesario
    # Para producción, asegúrate de poner debug=False y usar un servidor WSGI como Gunicorn
    app.run(debug=True, host='0.0.0.0', port=5000)
