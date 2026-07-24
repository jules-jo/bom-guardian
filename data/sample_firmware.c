/* Sample firmware for the Silicon Sentinel demo: STM32H743 sensor node. */

#include "stm32h7xx_hal.h"

I2C_HandleTypeDef hi2c1;
DMA_HandleTypeDef hdma_i2c1_rx;
UART_HandleTypeDef huart3;

static void sensors_init(void)
{
    hi2c1.Instance = I2C1;
    hi2c1.Init.Timing = 0x10C0ECFF;
    HAL_I2C_Init(&hi2c1);

    hdma_i2c1_rx.Instance = DMA1_Stream0;
    HAL_DMA_Init(&hdma_i2c1_rx);
}

static void console_init(void)
{
    huart3.Instance = USART3;
    huart3.Init.BaudRate = 115200;
    HAL_UART_Init(&huart3);
}

int main(void)
{
    HAL_Init();
    sensors_init();
    console_init();
    HAL_QSPI_Init(0);

    while (1) {
        HAL_I2C_Master_Receive(&hi2c1, 0x68 << 1, 0, 6, 100);
    }
}
