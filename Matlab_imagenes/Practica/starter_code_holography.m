% =========================
% SCRIPT DE PRUEBA : Control basico de la camara
% ==============================

clear ; close all; clc;

% 1. INICIALIZACION
% Usa 'winvideo ' y el ID del dispositivo (1 suele ser laintegrada , 2 la USB )
ID_camara = 1;
disp (' Conectando ␣con␣la␣ camara ... ') ;
cam = videoinput ('winvideo', ID_camara ) ;

% Forzar que MATLAB devuelva la matriz en formato RGB estandar
cam . ReturnedColorSpace = 'rgb';

% 2. ENCUADRE ( Opcional )
% Abre una ventana de video en vivo para poder apuntar la camara
preview ( cam ) ;
disp (' Encuadra ␣tu␣ objetivo .␣ Capturando ␣en␣3␣ segundos ... ') ;
pause (3) ;

% 3. CAPTURA
% Toma una unica fotografia (un frame matricial )
img = getsnapshot ( cam ) ;

% 4. VISUALIZACION
% Cerramos la vista previa y mostramos la foto estatica capturada
closepreview ( cam ) ;
figure ('Name', 'Prueba ␣de␣ Captura') ;
imshow ( img ) ;
title ('Imagen ␣ Capturada ␣ Exitosamente') ;

% 5. LIMPIEZA Y LIBERACION DE HARDWARE ( CRITICO )
% Si no haces esto , tendras que reiniciar MATLAB para volver a usar la camara
delete ( cam ) ; % Borra el objeto del hardware
clear cam ; % Borra la variable del Workspace
disp ('Camara ␣ desconectada ␣y␣ liberada ␣ correctamente .') ;


