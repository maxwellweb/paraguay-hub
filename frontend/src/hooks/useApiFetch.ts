
import { useState, useCallback } from 'react';
import axios, { AxiosError } from 'axios';
import type { Method } from 'axios';

// --- Interfaces de Tipado ---

// La interfaz del resultado se mantiene genérica para los datos <T>
interface UseApiFetchResult<T> {
    data: T | null;
    loading: boolean;
    error: string | null;
    // Función de solicitud flexible: recibe el método, el endpoint, y datos opcionales
    executeRequest: (
        method: Method, // 'get', 'post', 'put', 'delete', etc.
        endpoint: string,
        dataPayload?: any // Datos a enviar en POST/PUT
    ) => Promise<T | null>;
}

// URL base de tu backend
const BASE_URL: string = import.meta.env.VITE_API_BASE_URL;

/**
 * Hook flexible para realizar peticiones (GET, POST, etc.) a la API de FastAPI.
 * La solicitud no se ejecuta al cargar, sino cuando se llama a executeRequest.
 */
export const useApiFetch = <T>(): UseApiFetchResult<T> => {
    // Estados tipados
    const [data, setData] = useState<T | null>(null);
    const [loading, setLoading] = useState<boolean>(false); // Inicializado a false, ya que no se ejecuta al cargar
    const [error, setError] = useState<string | null>(null);

    // Función de ejecución de la solicitud
    const executeRequest = useCallback(async (
        method: Method, 
        endpoint: string,
        dataPayload?: any
    ): Promise<T | null> => {
        setLoading(true);
        setError(null);
        
        try {
            const url: string = `${BASE_URL}${endpoint}`;
            
            // 💡 Uso de Axios: Configuración dinámica de la solicitud
            const response = await axios.request<T>({
                method: method,
                url: url,
                data: dataPayload, // El body para POST/PUT
                // params: si necesitas parámetros de consulta para GET
            });

            setData(response.data);
            return response.data;

        } catch (err) {
            const axiosError = err as AxiosError;
            console.error(`Error en la solicitud ${method.toUpperCase()} a ${endpoint}:`, axiosError);
            
            if (axiosError.response) {
                 const status: number = axiosError.response.status;
                 const detail = (axiosError.response.data as any)?.detail || `Error desconocido del servidor (${status}).`;
                 setError(`Error ${status}: ${detail}`);
            } else {
                 setError("Error de conexión. Asegúrate de que FastAPI esté corriendo.");
            }
            setData(null);
            return null; // Devuelve null en caso de error
        } finally {
            setLoading(false);
        }
    }, []); // No tiene dependencias, es una función pura para la lógica de fetching

    // IMPORTANTE: Este hook no tiene useEffect para auto-ejecución

    return { data, loading, error, executeRequest };
};