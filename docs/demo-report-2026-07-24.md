# BOM Guardian Report
**6 components analyzed — 1 high risk.**

## 🔴 MPU-6050 — HIGH
*TDK InvenSense 6-axis IMU*

### Lifecycle
STATUS: EOL

- **Current lifecycle status**  
  - TDK’s official product page for MPU-6050 lists **Product Status: “Obsolete”**, with a note “Recommended Alternate Part No.: ICM-42670-P (Interchangeability is not guaranteed.)”. [[1]]
  - A major distributor (Digi-Key) also marks the MPU-6050 as **“Obsolete – This product is no longer manufactured.”** [[2]]
  - Earlier, at least one distributor (Mouser) showed the part as **NRND (Not recommended for new designs)** before it went obsolete. [[3]]
  → Taken together, these indicate the device is **end‑of‑life / no longer in production**.

- **PDN / PCN / EOL announcements**  
  - In the information gathered so far, no **official, part-specific Product Discontinuance Notice (PDN), Product Change Notice (PCN), or dated EOL announcement** for the MPU‑6050 itself was located on TDK/InvenSense public sites.  
  - An InvenSense store/news page provides a formal EOL notice with dates for other IMUs (MPU‑9250/9250M/9255) but does **not** mention MPU‑6050 in that EOL notice. [[4]]
  - Therefore, the EOL status for MPU‑6050 is established by **current official product status (“Obsolete”)** on TDK’s product page [[1]] and **matching distributor lifecycle flags** [[2]], not by a publicly found PDN document in the collected data.

- **Recommended replacements (near drop-in / functional alternatives)**  
  From TDK and distributor data:

  1. **ICM‑42670‑P (TDK InvenSense)**  
     - Listed directly on TDK’s MPU‑6050 product page as: “Recommended Alternate Part No.: ICM‑42670‑P (Interchangeability is not guaranteed.)”. [[1]]
     - Also appears as a suggested alternative on Digi-Key for the MPU‑6050. [[2]]
     - Same vendor, 6‑axis accel/gyro IMU; not pin‑ or register‑compatible, but intended as a successor device.

  2. **ICM‑42688‑P (TDK InvenSense)**  
     - Shown by Digi-Key in the “You may also be interested in” / alternative suggestions list for MPU‑6050. [[2]]
     - Higher‑performance 6‑axis IMU; again, **not** a drop‑in, but a near‑functional replacement from the same family.

  3. **BMI270 (Bosch Sensortec)**  
     - Also listed by Digi-Key in the alternative suggestions for the obsolete MPU‑6050. [[2]]
     - Competing 6‑axis IMU; requires full electrical, mechanical, and firmware re‑design; only a **functional** alternative.

- **Design implications**  
  - Because TDK explicitly warns that interchangeability of ICM‑42670‑P with MPU‑6050 is **not guaranteed** [[1]], all the above should be treated as **re‑design candidates**, not drop‑in replacements.  
  - For safety‑critical or volume designs, obtain the latest datasheets and migration guidance from TDK and validate pinout, register map, performance, and software changes.

- [MPU-6050 : Detailed Information | Sensors and Sensor Systems - ...](https://product.tdk.com/en/search/sensor/mortion-inertial/imu/info?part_no=MPU-6050) — | Product Status | Obsolete Recommended Alternate Part No. : ICM-42670-P \(Interchangeability is not guaranteed.\) |
- [MPU-6050 TDK InvenSense | IMUs \(Inertial Measurement Units\) | DigiKey](https://www.digikey.com/en/products/detail/tdk-invensense/MPU-6050/4038009) — Part Status Obsolete

Obsolete

This product is no longer manufactured.

You May Also Be Interested In

10 Items

SEN0142 6 DOF SENSOR - MPU6050 DFRobot $12.900…
- [MPU-6050 TDK InvenSense | Mouser](https://www.mouser.com/ProductDetail/TDK-InvenSense/MPU-6050/?qs=u4fy/sgLU9O14B5JgyQFvg%3D%3D) — MPU-6050 TDK InvenSense IMUs - Inertial Measurement Units 6-Axis MEMS MotionTracking Device with DMP datasheet, inventory, & pricing.
NRND: Not recommended for…
- [TDK InvenSense from InvenSense Online Store](https://store.invensense.com/manufacturer/invensense) — InvenSense: MEMS-based motion processing products including single, dual, triple, six and nine axis gyroscopes.
EOL Notification for MPU-9250, MPU-9250M, MPU-92…

### Errata
No published errata documents surfaced in search.

### Availability
No supply-risk signals in the last month.

## 🟡 EP2C5T144C8N — MEDIUM
*Intel/Altera Cyclone II FPGA*

### Lifecycle
STATUS: NRND

Lifecycle status  
- The EP2C5T144C8N is a Cyclone II FPGA device. A 2019 Intel community thread on Cyclone II (devices EP2C20F256I8N and EP2C8F256I8N) states that “Intel is not recommending cyclone II for new designs,” which corresponds to an NRND (Not Recommended for New Designs) lifecycle status for the family, not just a single device. [[1]]
- In that same thread, an engineer notes that any formal end‑of‑life information would appear in Intel’s official discontinuance/PCN/PDN listings and advises checking suppliers, implying that no EOL/PDN for Cyclone II was in effect at that time. [[1]]
- A 2024 article on Intel’s (Altera’s) FPGA strategy reports that Intel is “extending the lifetime of its MAX and Cyclone devices out to 2040,” guaranteeing at least 15 years of supply across the MAX and Cyclone portfolio. This extension is framed as applying broadly to MAX and Cyclone families to ensure long-term supply, not just to the newest generations, which supports the view that older Cyclone families such as Cyclone II remain supported for existing designs even if not recommended for new ones. [[2]]
- A major distributor still lists EP2C5T144C8N (Cyclone II, 144‑LQFP) as an orderable FPGA device, which is consistent with a supported-but-NRND status rather than formal EOL. Distributor availability alone is not proof of active status, but it aligns with the manufacturer statements that Cyclone devices remain in production for long-term supply. [[3]] [[2]] 

PCN / PDN / EOL findings  
- Within the information available here, no official Intel/Altera Product Discontinuance Notice (PDN), Product Change Notice (PCN), or explicit end‑of‑life announcement specifically naming EP2C5T144C8N or the Cyclone II family was found. The Intel community thread explicitly points out that EOL information would appear on Intel’s official notification channels, and no such reference is present in the retrieved material. [[1]]
- The only lifecycle‑specific manufacturer‑side statement in the gathered data is that Cyclone II is “not recommended for new designs” (NRND), with no production end date communicated. [[1]] 

Conclusion on current lifecycle  
- Based on:  
  • Intel’s own characterization of Cyclone II as “not recommended for new designs”; [[1]]
  • Absence (in the retrieved information) of any formal PDN/EOL for Cyclone II or EP2C5T144C8N; [[1]]
  • Intel/Altera’s public commitment to extended lifetime and supply for MAX and Cyclone devices out to at least 2040; [[2]]
  • Ongoing distributor listing of EP2C5T144C8N as an orderable part; [[3]] 

the most defensible classification for EP2C5T144C8N is:  
- In production and supported for existing designs,  
- Not recommended for new designs (NRND),  
- No confirmed manufacturer end‑of‑life / last‑time‑buy notice visible in the retrieved sources.

Replacement suggestions  
- From the data available here, no specific Intel-published list of pin‑compatible or “drop‑in” replacements for EP2C5T144C8N (Cyclone II, 144‑LQFP) was retrieved; the Intel community question about Cyclone II asks for pin‑compatible replacements, but the snippet does not show any concrete replacement part numbers from Intel. [[1]]
- Because no authoritative replacement mapping (e.g., Cyclone II → Cyclone III/IV/10LP equivalents in the same package and pinout) is visible in the gathered material, no specific drop‑in or near‑drop‑in replacement part numbers can be recommended here without going beyond the available evidence.

- [Cyclone II: End of production and recommended replacements - Intel ...](https://community.intel.com/t5/Programmable-Devices/Cyclone-II-End-of-production-and-recommended-replacements/m-p/699225) — We are using the following Cyclone II FPGAs in one of our designs: EP2C20F256I8N and EP2C8F256I8N. Intel is not recommending cyclone II for new designs. When wi…
- [Altera boosts FPGA for AI, extends lifetime .. ...](https://www.eenewseurope.com/en/altera-boosts-fpga-for-ai-extends-lifetime/) — Not only is it launching its mid-range 7nm Agilex 5 FPGA family with AI acceleration to take on the former Xilinx devices, but Intel’s Altera business is also m…
- [EP2C5T144C8N Altera | FPGAs \(Field Programmable Gate Array\) | DigiKey](https://www.digikey.com/en/products/detail/altera/EP2C5T144C8N/1084579) — Buy now, ships today. EP2C5T144C8N - Cyclone® II Field Programmable Gate Array \(FPGA\) IC 89 119808 4608 144-LQFP from Altera. View datasheets, pricing and avail…

### Errata
No published errata documents surfaced in search.

### Availability
No supply-risk signals in the last month.

## 🟢 STM32H743ZIT6 — LOW
*STMicroelectronics Cortex-M7 MCU 480MHz*

### Lifecycle
STATUS: ACTIVE

- ST’s official product page for STM32H743ZI lists the specific ordering code STM32H743ZIT6 with “Marketing Status: Active.” The tape‑and‑reel variant STM32H743ZIT6TR is also explicitly marked “Active.” [[1, 2, 3]]
- The ST eStore pages for STM32H743ZIT6 and STM32H743ZIT6TR show them as orderable devices and label the devices as “Active,” indicating they are in current production and available directly from ST, not only via distributors. [[4, 5]]
- The STM32H743/753 line and the broader STM32H7 series are presented on ST’s current portfolio pages as active product families with ongoing promotion (feature descriptions, “find products,” documentation and tools). No lifecycle warnings (NRND, last‑time‑buy, or obsolete) are shown for the STM32H743 family on these official product-family pages. [[6, 7, 8]] 

PCN / PDN / EOL / NRND findings

- ST’s general product longevity statement promises 7–20 years of supply (including notification period) and states that end‑of‑life decisions are communicated via their standard Product/Process Change Notice and Product Termination/End‑of‑Life notifications. [[9]]
- ST’s support FAQ explains that product/process changes and end‑of‑life are communicated via formal notifications; customers can request confirmation of notifications for specific part numbers. [[10]]
- A community thread about an STM32H7 CPU speed increase mentions that a Product Change Notification (PCN) was issued for a revision change (Rev Y → Rev V) of STM32H7 devices, but this is a silicon revision enhancement, not a product discontinuation or NRND notice. [[11]]
- Another PCN example found (PCN MDG/22/13640) concerns STM32G0 products, not STM32H743, showing that ST does publish formal PCNs but with no indication that an STM32H743 PDN exists in the same channel. [[12]] 

Based on the searches performed:

- No official Product Discontinuance Notice (PDN), Product Termination Notice, or end‑of‑life announcement was found referencing STM32H743ZIT6 or the STM32H743/753 family. The only formal ST change documentation encountered is unrelated to this part family or concerns product enhancements, not discontinuation. [[11, 12, 13]]
- No official ST “Not Recommended for New Designs (NRND)” designation was found for STM32H743ZIT6 or for the STM32H743/753 line; the official product pages and eStore continue to show the marketing status as Active. [[1, 2, 6]] 

Clarifying potentially confusing signals

- An ST community post notes that the NUCLEO‑H743ZI2 development board is flagged as “obsolete according to marketing status” inside STM32CubeIDE, but this refers to the board, not the MCU silicon itself. The MCU STM32H743ZIT6 on that board remains listed as Active on ST’s own product and eStore pages. [[14, 1, 4]]
- Distributor pages (Digi‑Key, TME, etc.) show ongoing listings and stock for STM32H743ZIT6, but lifecycle status is taken only from ST’s own marketing‑status fields, not from distributor availability, as requested. [[15, 16, 1]] 

Summary

- Current lifecycle status of STM32H743ZIT6: ACTIVE according to ST’s official product and eStore pages (Marketing Status: Active). [[1, 2, 4]]
- No ST Product Discontinuance Notification (PDN), no end‑of‑life notice, and no NRND marking were found for STM32H743ZIT6 or the STM32H743/753 family in the publicly accessible documentation and community channels searched. [[11, 12, 13]]
- ST’s general longevity policy indicates a 7–20‑year commitment with formal notification before EOL, and there is no sign yet of such notifications for this device family. [[9]] 

Because the part is not NRND or EOL, no replacement recommendations are necessary.

- [STM32H743ZI | Product - STMicroelectronics](https://st.com/en/microcontrollers/stm32h743zi.html) — STM32H742xI/G and STM32H743xI/G devices are based on the high-performance Arm® Cortex®-M7 32-bit RISC core operating at up to 480 MHz.
STM32H743ZIT6 · Package:…
- [STM32H743ZI | Product - STMicroelectronics](https://www.st.com/en/microcontrollers-microprocessors/stm32h743zi.html) — STM32H742xI/G and STM32H743xI/G devices are based on the high-performance Arm® Cortex®-M7 32-bit RISC core operating at up to 480 MHz.
STM32H743ZIT6 · Package:…
- [STM32H743ZI - High-performance and DSP with DP-FPU, ...](https://www.st.com/content/st_com/en/products/microcontrollers-microprocessors/stm32-32-bit-arm-cortex-mcus/stm32-high-performance-mcus/stm32h7-series/stm32h743-753/stm32h743zi.html) — STM32H742xI/G and STM32H743xI/G devices are based on the high-performance Arm® Cortex®-M7 32-bit RISC core operating at up to 480 MHz.
STM32H743ZIT6 · Package:…
- [Buy STM32H743ZIT6 - ST Online Store](https://estore.st.com/en/stm32h743zit6-cpn.html) — Order now STM32H743ZIT6 direct from STMicroelectronics eStore. Prices and availability in real-time, fast shipping.
High-performance and DSP with DP-FPU, Arm Co…
- [STM32H743ZIT6TR - eStore - STMicroelectronics](https://estore.st.com/en/stm32h743zit6tr-cpn.html) — Buy STM32H743ZIT6TR, High-performance and DSP with DP-FPU, Arm Cortex-M7 MCU with 2MBytes of Flash memory, 1MB RAM, 480 MHz CPU, Art Accelerator, L1 cache, exte…

### Errata
Published errata/advisories found: Errata sheet; stm32h742 stm32h743 Device Limitations Stmicroelectronics | PDF ...

- [Errata sheet](https://www.st.com/resource/en/errata_sheet/es0392-stm32h742xig-stm32h743xig-stm32h750xb-stm32h753xi-device-errata-stmicroelectronics.pdf) — This document applies to the part numbers of STM32H742xI/G, STM32H743xI/G, STM32H750xB, STM32H753xI devices and · the device variants as stated in this page
- [stm32h742 stm32h743 Device Limitations Stmicroelectronics | PDF ...](https://www.scribd.com/document/636945049/stm32h742-stm32h743-device-limitations-stmicroelectronics) — stm32h742-stm32h743-device-limitations-stmicroelectronics - Free download as PDF File \(.pdf\), Text File \(.txt\) or read online for free. STM32H742xI/G and STM32H…

### Availability
No supply-risk signals in the last month.

## 🟢 ATMEGA328P-PU — LOW
*Microchip 8-bit AVR MCU*

### Lifecycle
STATUS: ACTIVE

Lifecycle status  
- Microchip’s official product page lists ATmega328P with orderable part numbers including ATMEGA328P‑PU, shown in stock for purchase, with no NRND or EOL flag. [[1]] [[1]]
- An industry lifecycle analysis (Findchips blog, June 29, 2026) reports that Microchip Direct shows a *projected* end‑of‑life (EOL) date of 2040‑11‑04 for ATMEGA328P‑PU and that Rochester Electronics lists the device as Active. It explicitly notes that “No NRND or EOL flag appears across the authorized listings on Findchips as of June 23, 2026.” [[2]]
- Microchip’s AVR8 picoPower overview still references ATmega328P‑P family devices as current products. [[3]] 

Conclusion: Based on manufacturer information and cross‑checked lifecycle analysis, ATMEGA328P‑PU is currently an **active** Microchip product (not NRND, not EOL), despite some distributors’ commercial decisions.

Distributor NRND / “discontinued” flags (not manufacturer PDNs)  
- Mouser’s page for ATMEGA328P‑PU labels it “NRND: Not recommended for new designs,” even though it continues to sell the part and link to Microchip documentation. [[4]]
- Similar NRND labels appear on Mouser for related package codes ATMEGA328P‑AN and ATMEGA328P‑AU. [[5]] [[6]]
- OnlineComponents states “This product is discontinued, but still in stock,” referring to ATMEGA328P‑PU, but this is a distributor‑level status; it is not an official Microchip PDN. [[7]] 

These NRND/discontinued indications are therefore distributor policy, not evidence of a Microchip NRND/EOL announcement.

Manufacturer PCNs / errata involving ATmega328P family  
(These are Product Change Notices and documentation changes, not discontinuance notices.)

1. Die change PCN (Atmel → Microchip era)  
- Mouser hosts an Atmel Product Change Notification “PCN for mega48/88/168/328 die change,” reference WC154601, dated 2015‑11‑17. This PCN covers the ATmega48/88/168/328 family and describes a die change, not a discontinuation. [[8]] 

2. Silicon errata & datasheet clarification PCNs  
- Microchip published “ATmega48A/PA/88A/PA/168A/PA/328/P Silicon Errata and Data Sheet Clarification,” which explicitly states that the ATmega48A/PA/88A/PA/168A/PA/328/P devices received conform functionally to the device described and that issues are documented for future revisions. [[9]]
- Farnell and Mouser each re‑host this as part of Product Change Notification entries (e.g., PCN IDs SYST‑12WUIM914 and SYST‑17ZAXF644), describing the release of updated silicon errata and datasheet clarification documents for ATmega48A/PA/88A/PA/168A/PA/328/P. [[10]] [[11]] [[12]] 

3. Additional PCNs referenced on distributor pages  
- Mouser’s ATMEGA328P‑PU page lists multiple Microchip/Atmel Product Change Notification PDFs (including those above and others such as bonding‑wire changes), all under the ATmega48A/PA/88A/PA/168A/PA/328/P family. These are standard manufacturing or documentation changes, not PDNs. [[4]] 

Product Discontinuance Notifications (PDN) / EOL announcements / NRND from manufacturer  
- No official Microchip Product Discontinuance Notification specific to ATMEGA328P‑PU or the ATmega328P family was found in the gathered information. Instead, available notices are PCNs for die changes, bonding‑wire changes, and errata/datasheet clarifications. [[9]] [[10]] [[11]] [[12]] [[8]]
- The Findchips lifecycle article explicitly states that Microchip Direct lists only projected EOL dates (around 2040) and that no NRND or EOL flags are present on authorized listings as of mid‑2026. [[2]] 

Replacements (only relevant if user chooses to migrate despite active status)  
Even though the part is active, many distributors are marking it NRND for design‑in. For future‑proof designs within the same general ecosystem, commonly considered near‑drop‑in or migration targets (not mandated by Microchip PDNs) include:  

- ATmega328PB (same AVR core with additional peripherals; different device ID and slightly different pinout/feature set, so not a strict drop‑in but a close architectural successor used in many designs). [[2]]
- Other newer AVR options (e.g., tinyAVR or megaAVR 0‑series) and PIC microcontrollers are mentioned in community discussions as migration paths, but these are not pin‑compatible drop‑ins and require board redesign. [[13]] 

Summary  
- **No manufacturer PDN, NRND, or EOL announcement** has been identified for ATMEGA328P‑PU or its family in the information collected.  
- Microchip’s own listings and third‑party lifecycle analysis identify ATMEGA328P‑PU as **active**, with projected EOL well into the 2040 time frame and no NRND/EOL flags at the manufacturer level. [[1]] [[1]] [[2]]
- Several **PCNs** exist (die change in 2015 and various silicon errata/datasheet and bonding‑wire changes) but these are standard product updates. [[9]] [[10]] [[11]] [[12]] [[8]]
- Some distributors mark the device **NRND or “discontinued”** from their own commercial perspective, which does not correspond to a Microchip PDN or official lifecycle termination. [[4]] [[7]]

- [ATmega328P](https://www.microchip.com/en-us/product/atmega328p) — Download Datasheets. |. CAD Models. ATMEGA328P-PUATMEGA328P-ANATMEGA328P ... ATMEGA328P-PU. rohs. CAD. 28, SPDIP, -40C to +85C, TUBE, $2.10. In Stock Now.Read m…
- [ATmega328P \(2026\): Pinout, Packages & Live Findchips Stock](https://blog.findchips.com/atmega328p-2026-pinout-packages-availability/) — Yes. Microchip direct listings show a projected end of life date of 2040-11-04 for the ATMEGA328P-PU and ATMEGA328P-AU, and 2040-11-01 for the ATMEGA328P-MU. Ro…
- [AVR8 picoPower devices](https://support.microchip.com/s/article/AVR8-picoPower-devices) — AVR8 picoPower devices. Difference between P and non-P devices e.g. ATmega328P-PU and ATmega328-PU.Read more
- [ATMEGA328P-PU Microchip Technology | Mouser](https://www.mouser.com/en/ProductDetail/Microchip-Technology/ATMEGA328P-PU?qs=K8BHR703ZXguOQv3sKbWcg%3D%3D) — ATMEGA328P-PU Microchip Technology 8-bit Microcontrollers - MCU 32KB In-system Flash 20MHz 1.8V-5.5V datasheet, inventory, & pricing.
NRND: Not recommended for…
- [ATMEGA328P-AN Microchip Technology | Mouser India](https://www.mouser.in/ProductDetail/Microchip-Technology/ATMEGA328P-AN?qs=6Dg1WZIWLC6WK556tw8xAw%3D%3D) — ATMEGA328P-AN Microchip Technology 8-bit Microcontrollers - MCU AVR 32K FLSH 2K SRAM 1KB EE-20 MHZ 105C datasheet, inventory & pricing.
NRND: Not recommended fo…

### Errata
Published errata/advisories found: Errata © 2024 Microchip Technology Inc. and its subsidiaries ...

- [Errata © 2024 Microchip Technology Inc. and its subsidiaries ...](https://ww1.microchip.com/downloads/aemDocuments/documents/MCU08/ProductDocuments/Errata/ATmega328P-Auto-SilConErrataClarif-DS80001060.pdf) — this document will likely be addressed in future revisions of the ATmega328P Automotive devices. ... This document summarizes all the silicon errata issues from…

### Availability
No supply-risk signals in the last month.

## 🟢 DS3231SN — LOW
*Analog Devices RTC with TCXO*

### Lifecycle
STATUS: ACTIVE

• Current lifecycle status  
  – Analog Devices’ official DS3231 product page lists the device (including the DS3231SN# industrial SOIC‑16 variant) without any “Not Recommended for New Designs” or “Obsolete/EOL” markings, and presents it as a standard orderable part. [[1]]
  – The associated “Sample & Buy” page likewise treats DS3231 as an active product and provides ordering options for DS3231SN#. [[2]]
  – EngineerZone FAQ content explicitly discusses DS3231 and DS3231SN#T&R operation and FIT data as a current product, not a legacy or EOL device. [[3]] [[4]]
  – An external technical blog reports that Maxim (now Analog Devices) confirmed only the non‑RoHS DS3231 variants (without the “#” suffix) were being discontinued, while RoHS‑compliant versions such as DS3231SN# “are still being actively produced and are recommended for use in new designs.” [[5]] [[5]]

• PDN / PCN / EOL / NRND findings  
  – No public, official Analog Devices/Maxim Product Discontinuance Notification (PDN), Product Change Notice (PCN), or formal end‑of‑life (EOL) announcement specifically for DS3231SN or DS3231SN# was located in the retrieved information. The DS3231 datasheet carries only the usual generic “reserves the right to change” language, not a discontinuance notice. [[6]]
  – The blog article notes that Maxim’s internal EOL/NRND listing at that time showed some DS3231 variants as EOL/NRND, but explicitly distinguishes those from the RoHS “#” versions, which Maxim reportedly stated remain in production and recommended for new designs (statement dated in the blog post on 2020‑09‑27). [[5]]
  – None of the official Analog Devices DS3231 pages found include NRND flags for DS3231SN#/DS3231SN, and distributor listings (e.g., Newark) show DS3231SN# as a normal, orderable part but are not relied upon here as lifecycle authorities. [[1]] [[7]]

• Conclusion  
  – Based on the official Analog Devices product and ordering pages plus the reported manufacturer statement that only non‑RoHS DS3231 variants were discontinued, DS3231SN# (and thus the DS3231SN RoHS family member) is best classified as ACTIVE, with no evidence of NRND or EOL status in the information gathered. [[1]] [[2]] [[5]] [[5]]

- [DS3231 Datasheet and Product Info | Analog Devices](https://www.analog.com/en/products/ds3231.html) — The DS3231 is low-cost, extremely accurate I²C real-time clock \(RTC\) with an integrated temperature-compensated crystal oscillator \(TCXO\) and crystal. The devic…
- [DS3231 Sample & Buy | Analog Devices](https://www.analog.com/en/products/ds3231/sample-buy.html) — The DS3231 is low-cost, extremely accurate I²C real-time clock \(RTC\) with an integrated temperature-compensated crystal oscillator \(TCXO\) and crystal. The devic…
- [What is the expected ppm accuracy for the DS3231? - Documents - ...](https://ez.analog.com/clock_and_timing/w/documents/19193/what-is-the-expected-ppm-accuracy-for-the-ds3231) — What is the FIT rate of the DS3231SN#T&R for different temperatures? We expect +/-3.5ppm accuracy across the operational temperature range of -40C to +85C for t…
- [What is the function of pushbutton reset RST pin of DS3231SN? - ...](https://ez.analog.com/clock_and_timing/w/documents/22861/what-is-the-function-of-pushbutton-reset-rst-pin-of-ds3231sn) — What is the FIT rate of the DS3231SN#T&R for different temperatures? RST pin has two functions: 1. When VCC falls below VPF, RST is driven low. This is for moni…
- [The DS3231 is dead, long live the DS3231#! – HeyPete.com Blog](https://blog.heypete.com/2020/09/27/the-ds3231-is-dead-long-live-the-ds3231/) — I contacted Maxim and inquired what was going on, and the response was that the non-RoHS versions \(e.g. with lead solder\) are being discontinued, while the RoHS…

### Errata
Published errata/advisories found: ±5ppm, I2C Real-Time Clock DS3231M

- [±5ppm, I2C Real-Time Clock DS3231M](https://cdn.sparkfun.com/datasheets/Dev/Beagle/DS3231M.pdf) — Note: Some revisions of this device may incorporate deviations from published specifications known as errata.

### Availability
No supply-risk signals in the last month.

## 🟢 NE555P — LOW
*Texas Instruments Timer IC*

### Lifecycle
STATUS: ACTIVE

- TI product status  
  - The official TI datasheet ordering information table lists NE555P and related orderable variants (NE555P, NE555P.A, NE555PE4, NE555PE4.A, etc.) as “Active – Production” in the PDIP (P) 8‑pin package. [[1]]
  - TI’s product page for NE555/NE555P is live and shows NE555P as an orderable device in PDIP with no NRND, Last‑Time‑Buy, or Obsolete flag; it is treated as a standard active catalog part. [[2]] [[3]]
  - TI’s general product life‑cycle policy defines official statuses as Preview, Active, Not recommended for new designs (NRND), Last time buy, and Obsolete, and emphasizes long product lifetimes. There is no indication that NE555P has moved out of the “Active” category under this policy. [[4]]

- PDN/PCN/EOL/NRND findings for NE555P  
  - Within the information collected from TI and distributors, NE555P in PDIP shows only “Active/Production,” and no TI-issued Product Discontinuance Notification (PDN), Product Change Notice (PCN) specifically targeting NE555P, end‑of‑life notice, or NRND marking was found. [[1]] [[2]] [[3]]
  - Some distributor content simply relays TI’s datasheet and standard warranty/availability notice; this is generic “production data” language and not an obsolescence notice. [[5]]
  - A different device/packing variant, NE555DR (SOIC package), is marked by a distributor as “End of Life: Scheduled for obsolescence and will be discontinued by the manufacturer,” and that page links to TI PCN PDFs for SOIC devices; however, this is for NE555DR, not NE555P, and does not indicate discontinuance of the PDIP NE555P itself. [[6]]

- Summary  
  - Based on TI’s own datasheet ordering table and product page, NE555P (PDIP‑8) is currently in **Active / Production** status, not NRND or EOL. [[1]] [[2]] [[3]]
  - No official TI PDN, NE555P‑specific PCN indicating obsolescence, or NRND designation was found for NE555P in the gathered information. [[1]] [[2]] [[3]]

- Replacements  
  - Since NE555P is active, TI has not issued an end‑of‑life notice suggesting replacements, and drop‑in alternatives are not formally required.

- [xx555 Precision Timers 1 Features • Timing from microseconds ...](https://www.ti.com/lit/ds/symlink/ne555.pdf) — NE555P · Active · Production · PDIP \(P\) | 8 · 50 | TUBE · Yes · NIPDAU | SN · N/A for Pkg Type · 0 to 70 · NE555P · NE555P.A · Active · Production · PDIP \(P\) |…
- [NE555P](https://www.ti.com/product/NE555/part-details/NE555P) — NE555P - Single Precision Timer | P | 8 | 0 to 70 in a PDIP \(P\) package with 8 pins
Same as: NE555P.A · This part number is identical to the part number listed…
- [NE555 data sheet, product information and support | TI.com](https://www.ti.com/product/NE555) — TI’s NE555 is a Single Precision Timer. Find parameters, ordering and quality information
- [Product life cycle | TI.com](https://www.ti.com/support-quality/quality-policies-procedures/product-life-cycle.html) — TI designates the life cycle status of each TI product as Preview, Active, Not recommended for new designs \(NRND\), Last time buy or Obsolete.
At Texas Instrumen…
- [NE555P-Texas-Instruments-datasheet-7284017.pdf](https://datasheet.octopart.com/NE555P-Texas-Instruments-datasheet-7284017.pdf) — Please be aware that an important notice concerning availability, standard warranty, and use in critical applications of Texas · Instruments semiconductor produ…

### Errata
No published errata documents surfaced in search.

### Availability
No supply-risk signals in the last month.

