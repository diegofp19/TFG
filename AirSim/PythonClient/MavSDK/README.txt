1. Primero ejecutar PX4 y si hay problemas ejecutar el siguiente comando: ./.local/lib/python3.8/site-packages/mavsdk/bin/mavsdk_server udp://:14551 -p 50051
2. Cuando se ejecute el main para llevarlo a donde se desee, pulsar la tecla R en Unreal Engine cuando se quiera grabar y de nuevo R para para la grabación.
3. Coger la dirección de los frames y meterla en archivo video-converter.py para unirlos en un vídeo.
4. Con el vídeo anterior, ejecutar mainOpenCV.py (modificar parámetros según se requiera) y revisar posteriormente el csv que genera. 