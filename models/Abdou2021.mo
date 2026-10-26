within;
package Abdou2021
  "Dynamic Tritium Fuel Cycle Model Strictly Formulated per Abdou et al., Nucl. Fusion 61 (2021) 013001 (Section 3 & Appendix A)"

  record Baseline
    "Reference Parameters from Tables 1, 2, 3, and Table A.3 of Abdou et al. (2021)"
    // --- Table 1: Main plasma and sysem parameters ---
    constant Real Power(unit = "MW") = 3000.0 "Nominal fusion power (3 GW reference case, Table 1)";
    constant Real N_dot_burn_3GW(unit = "g/h") = 459.0 / 24.0 "Tritium burning rate for 3 GW plant (0.459 kg/day = 19.125 g/h, Table 1)";
    constant Real f_b(unit = "1") = 0.015 "Tritium burn fraction in the plasma (1.5% expected for first DEMOs, Table 1)";
    constant Real eta_f(unit = "1") = 0.25 "Fueling efficiency (25%, Table 1)";
    constant Real Lambda(unit = "1") = 1.18 "Required Tritium Breeding Ratio TBR_R (Lambda in Eq. A.1)";
    constant Real AF(unit = "1") = 1 "Reactor availability factor (AF = MTBF / (MTBF + MTTR), Eq. 3.11)";
    constant Real t_d(unit = "h") = 5.0 * 365.25 * 24.0 "Doubling time (5 years = 43830 h, Table 1)";
    constant Real t_r(unit = "h") = 24.0 "Reserve time (24 h, Table 1)";
    constant Real q_fail(unit = "1") = 0.25 "Fraction of the fuel cycle failing (25%, Table 1)";

// --- Radioactive decay constant ---
    constant Real lambda_decay(unit = "1/h") = 6.422e-6 "Tritium decay rate (half-life 12.32 yr, ~5.47%/yr)";

// --- Tables 2 & 3: Residence / processing times (tau_i, in hours) ---
    constant Real tau_1(unit = "h") = 24.0 "Comp 1: Breeding Zone (BZ) residence time (1 day, Table 3)";
    constant Real tau_2(unit = "h") = 24.0 "Comp 2: Tritium Extraction System (TES) processing time (1 day, Table 3)";
    constant Real tau_3(unit = "h") = 1000.0 / 3600.0 "Comp 3: First Wall (FW) residence time (1000 s, Table 3)";
    constant Real tau_4(unit = "h") = 1000.0 / 3600.0 "Comp 4: Divertor (DIV) residence time (1000 s, Table 3)";
    constant Real tau_5(unit = "h") = 1000.0 / 3600.0 "Comp 5: Heat Exchanger / Steam Generator (HX) residence time (1000 s, Table 3)";
    constant Real tau_6(unit = "h") = 240.0 "Comp 6: Coolant Purification System (CPS) processing time (10 days, Table 3)";
    constant Real tau_7(unit = "h") = 0.17 "Comp 7: Vacuum Pump residence time (~10-20 min, Sec. 9.1)";
    constant Real tau_8(unit = "h") = 0.33 "Comp 8: Fuel Clean-up (FCU) residence time";
    constant Real tau_9(unit = "h") = 3.50 "Comp 9: Isotope Separation System (ISS) processing time (such that IFC exhaust t_p = 4 h, Table 2)";
    constant Real tau_10(unit = "h") = 1.0 "Comp 10: Exhaust and Water Detritiation System (EDS/WDS) processing time (1 h, Table 2)";

// --- Table A.3: Flow rate fractions (f_{i-j}) and efficiencies (eta_i) ---
    constant Real f_1_5(unit = "1") = 1e-2 "Fraction of BZ outflow permeating to HX (f_{1-5}, Table A.3)";
    constant Real f_p_3(unit = "1") = 1e-4 "Fraction of injected T implanted into FW (f_{p-3}, Table A.3)";
    constant Real f_p_4(unit = "1") = 1e-4 "Fraction of injected T implanted into DIV (f_{p-4}, Table A.3)";
    constant Real f_5_3(unit = "1") = 0.6 "Fraction of recycled HX coolant directed to FW (f_{5-3}, Table A.3)";
    constant Real f_5_6(unit = "1") = 1e-2 "Fraction of HX coolant routed to CPS (f_{5-6}, Table A.3)";
    constant Real f_5_10(unit = "1") = 1e-4 "Fraction of HX coolant routed to EDS/WDS (f_{5-10}, Table A.3)";
    constant Real f_6_3(unit = "1") = 0.6 "Fraction of unrecovered CPS outflow directed to FW (f_{6-3}, Table A.3)";
    constant Real f_8_11(unit = "1") = 0.0 "Direct Internal Recycling (DIR) fraction from FCU to Storage (f_{8-11}, Table A.3 reference case = 0)";
    constant Real f_9_10(unit = "1") = 1e-1 "Fraction of ISS outflow routed to EDS/WDS (f_{9-10}, Table A.3)";
    constant Real eta_2(unit = "1") = 0.95 "TES tritium extraction efficiency (eta_2, Table A.3)";
    constant Real eta_6(unit = "1") = 0.95 "CPS tritium extraction efficiency (eta_6, Table A.3)";

// --- Appendix A: Non-radioactive loss fractions (epsilon_i) ---
    constant Real eps_zero(unit = "1") = 0.0 "Zero environmental loss for in-vessel & low-temp storage/fueling (eps_1,3,4,11,12 = 0)";
    constant Real eps_nom(unit = "1") = 1e-4 "Nominal non-radioactive loss fraction (eps_2,5,6,7,8,9,10 = 1e-4)";
  end Baseline;

  // ===========================================================================
  // Component 1: Breeding Zone (BZ) - Equation (A.1) & Table A.1
  // ===========================================================================
  model BZ "Component 1: Breeding Zone (Eq. A.1)"
    outer parameter Real time_scale "Time-base factor: 1 = hour-based, 3600 = second-based";
    Real inventory(unit = "g", start = 0, fixed = true) "Tritium inventory I_1 (I_1(0) = 0 per Eq. A.13)";
    Real S_1(unit = "g/h") "Tritium breeding source term S_1 = Lambda * N_dot_burn";
    Real outflow(unit = "g/h") "Total outflow I_1 / tau_1";

    parameter Real tau_1(unit = "h") = Baseline.tau_1 "Residence time tau_1";
    parameter Real lambda_decay(unit = "1/h") = Baseline.lambda_decay "Decay constant lambda";
    parameter Real epsilon_1(unit = "1") = Baseline.eps_zero "Non-radioactive loss fraction epsilon_1 = 0";
    parameter Real Lambda(unit = "1") = Baseline.Lambda "Required TBR (Lambda)";
    parameter Real f_1_5(unit = "1") = Baseline.f_1_5 "Fraction of outflow to Heat Exchanger (Comp 5)";
    protected
    parameter Real inv_T1(unit = "1/h") = (1 + epsilon_1) / tau_1 + lambda_decay "1 / T_1 per Eq. (A.13)";

  public
    Modelica.Blocks.Interfaces.RealInput N_dot_burn annotation(
      Placement(transformation(origin = {-120, 40}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {0, 110}, extent = {{-15, -15}, {15, 15}}, rotation = -90)));
    Modelica.Blocks.Interfaces.RealInput m_2_1 annotation(
      Placement(transformation(origin = {-120, -40}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {110, 40}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
    Modelica.Blocks.Interfaces.RealOutput m_1_2 annotation(
      Placement(transformation(origin = {110, 40}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {110, -40}, extent = {{-10, -10}, {10, 10}})));
    Modelica.Blocks.Interfaces.RealOutput m_1_5 annotation(
      Placement(transformation(origin = {110, -40}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {0, -110}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));

  equation
    S_1 = Lambda * N_dot_burn;
    outflow = inventory / tau_1;
// Eq. (A.1): dI_1/dt = Lambda * N_dot^- + (1 - eta_2) * (I_2 / tau_2) - I_1 / T_1
    der(inventory) = (S_1 + m_2_1 - inventory * inv_T1) / time_scale;
// Table A.1 outflows
    m_1_2 = (1 - f_1_5) * outflow;
    m_1_5 = f_1_5 * outflow;

    annotation(
      Icon(graphics = {
        Rectangle(fillColor = {144, 238, 144}, fillPattern = FillPattern.Solid, extent = {{-100, 100}, {100, -100}}),
        Text(origin = {0, 0}, extent = {{-80, 60}, {80, -60}}, textString = "1: BZ", fontName = "Arial")
      }));
  end BZ;

  // ===========================================================================
  // Component 2: Tritium Extraction System (TES) - Equation (A.2) & Table A.1
  // ===========================================================================
  model TES "Component 2: TES Unit (Eq. A.2)"
    outer parameter Real time_scale;
    Real inventory(unit = "g", start = 0, fixed = true) "Tritium inventory I_2 (I_2(0) = 0 per Eq. A.13)";
    Real outflow(unit = "g/h") "Total outflow I_2 / tau_2";

    parameter Real tau_2(unit = "h") = Baseline.tau_2 "Processing time tau_2";
    parameter Real lambda_decay(unit = "1/h") = Baseline.lambda_decay "Decay constant lambda";
    parameter Real epsilon_2(unit = "1") = Baseline.eps_nom "Non-radioactive loss fraction epsilon_2 = 1e-4";
    parameter Real eta_2(unit = "1") = Baseline.eta_2 "TES extraction efficiency eta_2 = 0.95";
    protected
    parameter Real inv_T2(unit = "1/h") = (1 + epsilon_2) / tau_2 + lambda_decay "1 / T_2 per Eq. (A.13)";

  public
    Modelica.Blocks.Interfaces.RealInput m_1_2 annotation(
      Placement(transformation(origin = {-120, 0}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {-110, -40}, extent = {{-10, -10}, {10, 10}})));
    Modelica.Blocks.Interfaces.RealOutput m_2_1 annotation(
      Placement(transformation(origin = {110, 40}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {-110, 40}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
    Modelica.Blocks.Interfaces.RealOutput m_2_9 annotation(
      Placement(transformation(origin = {110, -40}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {0, 110}, extent = {{-10, -10}, {10, 10}}, rotation = 90)));

  equation
    outflow = inventory / tau_2;
// Eq. (A.2): dI_2/dt = (1 - f_{1-5}) * (I_1 / tau_1) - I_2 / T_2
    der(inventory) = (m_1_2 - inventory * inv_T2) / time_scale;
// Table A.1 & Fig. A.1 outflows
    m_2_1 = (1 - eta_2) * outflow;
    m_2_9 = eta_2 * outflow;

    annotation(
      Icon(graphics = {
        Rectangle(fillColor = {173, 216, 230}, fillPattern = FillPattern.Solid, extent = {{-100, 100}, {100, -100}}),
        Text(origin = {0, 0}, extent = {{-80, 60}, {80, -60}}, textString = "2: TES", fontName = "Arial")
      }));
  end TES;

  // ===========================================================================
  // Component 3: First Wall (FW) - Equation (A.3) & Table A.1
  // ===========================================================================
  model FW "Component 3: First Wall (Eq. A.3)"
    outer parameter Real time_scale;
    Real inventory(unit = "g", start = 0, fixed = true) "Tritium inventory I_3 (I_3(0) = 0 per Eq. A.13)";
    Real outflow(unit = "g/h") "Total outflow I_3 / tau_3";

    parameter Real tau_3(unit = "h") = Baseline.tau_3 "Residence time tau_3";
    parameter Real lambda_decay(unit = "1/h") = Baseline.lambda_decay "Decay constant lambda";
    parameter Real epsilon_3(unit = "1") = Baseline.eps_zero "Non-radioactive loss fraction epsilon_3 = 0";
    protected
    parameter Real inv_T3(unit = "1/h") = (1 + epsilon_3) / tau_3 + lambda_decay "1 / T_3 per Eq. (A.13)";

  public
    Modelica.Blocks.Interfaces.RealInput m_p_3 annotation(
      Placement(transformation(origin = {-120, 60}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {-110, 0}, extent = {{-10, -10}, {10, 10}})));
    Modelica.Blocks.Interfaces.RealInput m_5_3 annotation(
      Placement(transformation(origin = {-120, 0}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {110, -40}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
    Modelica.Blocks.Interfaces.RealInput m_6_3 annotation(
      Placement(transformation(origin = {-120, -60}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {0, -110}, extent = {{-10, -10}, {10, 10}}, rotation = 90)));
    Modelica.Blocks.Interfaces.RealOutput m_3_5 annotation(
      Placement(transformation(origin = {110, 0}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {110, 40}, extent = {{-10, -10}, {10, 10}})));

  equation
    outflow = inventory / tau_3;
// Eq. (A.3): dI_3/dt = m_{p-3} + m_{5-3} + m_{6-3} - I_3 / T_3
    der(inventory) = (m_p_3 + m_5_3 + m_6_3 - inventory * inv_T3) / time_scale;

    m_3_5 = outflow;

    annotation(
      Icon(graphics = {
        Rectangle(fillColor = {173, 216, 230}, fillPattern = FillPattern.Solid, extent = {{-100, 100}, {100, -100}}),
        Text(origin = {0, 0}, extent = {{-80, 60}, {80, -60}}, textString = "3: FW", fontName = "Arial")
      }));
  end FW;

  // ===========================================================================
  // Component 4: Divertor (DIV) - Equation (A.4) & Table A.1
  // ===========================================================================
  model DIV "Component 4: Divertor (Eq. A.4)"
    outer parameter Real time_scale;
    Real inventory(unit = "g", start = 0, fixed = true) "Tritium inventory I_4 (I_4(0) = 0 per Eq. A.13)";
    Real outflow(unit = "g/h") "Total outflow I_4 / tau_4";

    parameter Real tau_4(unit = "h") = Baseline.tau_4 "Residence time tau_4";
    parameter Real lambda_decay(unit = "1/h") = Baseline.lambda_decay "Decay constant lambda";
    parameter Real epsilon_4(unit = "1") = Baseline.eps_zero "Non-radioactive loss fraction epsilon_4 = 0";
    protected
    parameter Real inv_T4(unit = "1/h") = (1 + epsilon_4) / tau_4 + lambda_decay "1 / T_4 per Eq. (A.13)";

  public
    Modelica.Blocks.Interfaces.RealInput m_p_4 annotation(
      Placement(transformation(origin = {-120, 60}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {-110, 0}, extent = {{-10, -10}, {10, 10}})));
    Modelica.Blocks.Interfaces.RealInput m_5_4 annotation(
      Placement(transformation(origin = {-120, 0}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {110, -20}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
    Modelica.Blocks.Interfaces.RealInput m_6_4 annotation(
      Placement(transformation(origin = {-120, -60}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {110, -60}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
    Modelica.Blocks.Interfaces.RealOutput m_4_5 annotation(
      Placement(transformation(origin = {110, 0}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {110, 40}, extent = {{-10, -10}, {10, 10}})));

  equation
    outflow = inventory / tau_4;
// Eq. (A.4): dI_4/dt = m_{p-4} + m_{5-4} + m_{6-4} - I_4 / T_4
    der(inventory) = (m_p_4 + m_5_4 + m_6_4 - inventory * inv_T4) / time_scale;

    m_4_5 = outflow;

    annotation(
      Icon(graphics = {
        Rectangle(fillColor = {255, 182, 193}, fillPattern = FillPattern.Solid, extent = {{-100, 100}, {100, -100}}),
        Text(origin = {0, 0}, extent = {{-80, 60}, {80, -60}}, textString = "4: DIV", fontName = "Arial")
      }));
  end DIV;

  // ===========================================================================
  // Component 5: Heat Exchanger (HX) - Equation (A.5) & Table A.1
  // ===========================================================================
  model HX "Component 5: Heat Exchanger / Steam Generator (Eq. A.5)"
    outer parameter Real time_scale;
    Real inventory(unit = "g", start = 0, fixed = true) "Tritium inventory I_5 (I_5(0) = 0 per Eq. A.13)";
    Real outflow(unit = "g/h") "Total outflow I_5 / tau_5";

    parameter Real tau_5(unit = "h") = Baseline.tau_5 "Residence time tau_5";
    parameter Real lambda_decay(unit = "1/h") = Baseline.lambda_decay "Decay constant lambda";
    parameter Real epsilon_5(unit = "1") = Baseline.eps_nom "Non-radioactive loss fraction epsilon_5 = 1e-4";
    parameter Real f_5_3(unit = "1") = Baseline.f_5_3 "Fraction to FW (f_{5-3})";
    parameter Real f_5_6(unit = "1") = Baseline.f_5_6 "Fraction to CPS (f_{5-6})";
    parameter Real f_5_10(unit = "1") = Baseline.f_5_10 "Fraction to EDS/WDS (f_{5-10})";
    protected
    parameter Real inv_T5(unit = "1/h") = (1 + epsilon_5) / tau_5 + lambda_decay "1 / T_5 per Eq. (A.13)";

  public
    Modelica.Blocks.Interfaces.RealInput m_1_5 annotation(
      Placement(transformation(origin = {-120, 60}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {0, 110}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
    Modelica.Blocks.Interfaces.RealInput m_3_5 annotation(
      Placement(transformation(origin = {-120, 0}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {-110, 60}, extent = {{-10, -10}, {10, 10}})));
    Modelica.Blocks.Interfaces.RealInput m_4_5 annotation(
      Placement(transformation(origin = {-120, -60}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {-110, -20}, extent = {{-10, -10}, {10, 10}})));

    Modelica.Blocks.Interfaces.RealOutput m_5_3 annotation(
      Placement(transformation(origin = {110, 60}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {-110, 20}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
    Modelica.Blocks.Interfaces.RealOutput m_5_4 annotation(
      Placement(transformation(origin = {110, 20}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {-110, -60}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
    Modelica.Blocks.Interfaces.RealOutput m_5_6 annotation(
      Placement(transformation(origin = {110, -20}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {0, -110}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
    Modelica.Blocks.Interfaces.RealOutput m_5_10 annotation(
      Placement(transformation(origin = {110, -60}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {110, -60}, extent = {{-10, -10}, {10, 10}})));

  equation
    outflow = inventory / tau_5;
// Eq. (A.5): dI_5/dt = f_{1-5}*(I_1/tau_1) + I_3/tau_3 + I_4/tau_4 - I_5/T_5
    der(inventory) = (m_1_5 + m_3_5 + m_4_5 - inventory * inv_T5) / time_scale;
// Table A.1 outflows
    m_5_3 = f_5_3 * (1 - f_5_6) * (1 - f_5_10) * outflow;
    m_5_4 = (1 - f_5_3) * (1 - f_5_6) * (1 - f_5_10) * outflow;
    m_5_6 = f_5_6 * (1 - f_5_10) * outflow;
    m_5_10 = f_5_10 * outflow;

    annotation(
      Icon(graphics = {
        Rectangle(fillColor = {255, 228, 196}, fillPattern = FillPattern.Solid, extent = {{-100, 100}, {100, -100}}),
        Text(origin = {0, 0}, extent = {{-80, 60}, {80, -60}}, textString = "5: HX", fontName = "Arial")
      }));
  end HX;

  // ===========================================================================
  // Component 6: Coolant Purification System (CPS) - Equation (A.6) & Table A.1
  // ===========================================================================
  model CPS "Component 6: CPS Unit (Eq. A.6)"
    outer parameter Real time_scale;
    Real inventory(unit = "g", start = 0, fixed = true) "Tritium inventory I_6 (I_6(0) = 0 per Eq. A.13)";
    Real outflow(unit = "g/h") "Total outflow I_6 / tau_6";

    parameter Real tau_6(unit = "h") = Baseline.tau_6 "Processing time tau_6";
    parameter Real lambda_decay(unit = "1/h") = Baseline.lambda_decay "Decay constant lambda";
    parameter Real epsilon_6(unit = "1") = Baseline.eps_nom "Non-radioactive loss fraction epsilon_6 = 1e-4";
    parameter Real f_6_3(unit = "1") = Baseline.f_6_3 "Fraction of unrecovered outflow to FW (f_{6-3})";
    parameter Real eta_6(unit = "1") = Baseline.eta_6 "CPS extraction efficiency eta_6 = 0.95";
    protected
    parameter Real inv_T6(unit = "1/h") = (1 + epsilon_6) / tau_6 + lambda_decay "1 / T_6 per Eq. (A.13)";

  public
    Modelica.Blocks.Interfaces.RealInput m_5_6 annotation(
      Placement(transformation(origin = {-120, 0}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {0, 110}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
    Modelica.Blocks.Interfaces.RealOutput m_6_3 annotation(
      Placement(transformation(origin = {110, 60}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {-110, 40}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
    Modelica.Blocks.Interfaces.RealOutput m_6_4 annotation(
      Placement(transformation(origin = {110, 0}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {-110, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
    Modelica.Blocks.Interfaces.RealOutput m_6_9 annotation(
      Placement(transformation(origin = {110, -60}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {-110, -40}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));

  equation
    outflow = inventory / tau_6;
// Eq. (A.6): dI_6/dt = f_{5-6}*(1 - f_{5-10})*(I_5/tau_5) - I_6/T_6
    der(inventory) = (m_5_6 - inventory * inv_T6) / time_scale;
// Table A.1 & Fig. A.1 outflows
    m_6_3 = f_6_3 * (1 - eta_6) * outflow;
    m_6_4 = (1 - f_6_3) * (1 - eta_6) * outflow;
    m_6_9 = eta_6 * outflow;

    annotation(
      Icon(graphics = {
        Rectangle(fillColor = {216, 191, 216}, fillPattern = FillPattern.Solid, extent = {{-100, 100}, {100, -100}}),
        Text(origin = {0, 0}, extent = {{-80, 60}, {80, -60}}, textString = "6: CPS", fontName = "Arial")
      }));
  end CPS;

  // ===========================================================================
  // Component 7: Vacuum Pump - Equation (A.7) & Table A.2
  // ===========================================================================
  model VacuumPump "Component 7: Vacuum Pump (Eq. A.7)"
    outer parameter Real time_scale;
    Real inventory(unit = "g", start = 0, fixed = true) "Tritium inventory I_7 (I_7(0) = 0 per Eq. A.13)";
    Real outflow(unit = "g/h") "Total outflow I_7 / tau_7";

    parameter Real tau_7(unit = "h") = Baseline.tau_7 "Residence time tau_7";
    parameter Real lambda_decay(unit = "1/h") = Baseline.lambda_decay "Decay constant lambda";
    parameter Real epsilon_7(unit = "1") = Baseline.eps_nom "Non-radioactive loss fraction epsilon_7 = 1e-4";
    protected
    parameter Real inv_T7(unit = "1/h") = (1 + epsilon_7) / tau_7 + lambda_decay "1 / T_7 per Eq. (A.13)";

  public
    Modelica.Blocks.Interfaces.RealInput m_p_7 annotation(
      Placement(transformation(origin = {-120, 0}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {0, 110}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
    Modelica.Blocks.Interfaces.RealOutput m_7_8 annotation(
      Placement(transformation(origin = {110, 0}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {-110, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));

  equation
    outflow = inventory / tau_7;
// Eq. (A.7): dI_7/dt = (1 - eta_f*f_b - f_{p-3} - f_{p-4}) * (N_dot^- / (eta_f*f_b)) - I_7/T_7
    der(inventory) = (m_p_7 - inventory * inv_T7) / time_scale;

    m_7_8 = outflow;

    annotation(
      Icon(graphics = {
        Rectangle(fillColor = {255, 255, 0}, fillPattern = FillPattern.Solid, extent = {{-100, 100}, {100, -100}}),
        Text(origin = {0, 0}, extent = {{-80, 60}, {80, -60}}, textString = "7: Pump", fontName = "Arial")
      }));
  end VacuumPump;

  // ===========================================================================
  // Component 8: Fuel Clean-up (FCU) - Equation (A.8) & Table A.2
  // ===========================================================================
  model FCU "Component 8: Fuel Clean-up (Eq. A.8)"
    outer parameter Real time_scale;
    Real inventory(unit = "g", start = 0, fixed = true) "Tritium inventory I_8 (I_8(0) = 0 per Eq. A.13)";
    Real outflow(unit = "g/h") "Total outflow I_8 / tau_8";

    parameter Real tau_8(unit = "h") = Baseline.tau_8 "Residence time tau_8";
    parameter Real lambda_decay(unit = "1/h") = Baseline.lambda_decay "Decay constant lambda";
    parameter Real epsilon_8(unit = "1") = Baseline.eps_nom "Non-radioactive loss fraction epsilon_8 = 1e-4";
    parameter Real f_8_11(unit = "1") = Baseline.f_8_11 "DIR fraction to Storage (f_{8-11})";
    protected
    parameter Real inv_T8(unit = "1/h") = (1 + epsilon_8) / tau_8 + lambda_decay "1 / T_8 per Eq. (A.13)";

  public
    Modelica.Blocks.Interfaces.RealInput m_7_8 annotation(
      Placement(transformation(origin = {-120, 0}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {110, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
    Modelica.Blocks.Interfaces.RealOutput m_8_9 annotation(
      Placement(transformation(origin = {110, -40}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {-110, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
    Modelica.Blocks.Interfaces.RealOutput m_8_11 annotation(
      Placement(transformation(origin = {110, 40}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {0, 110}, extent = {{-10, -10}, {10, 10}}, rotation = 90)));

  equation
    outflow = inventory / tau_8;
// Eq. (A.8): dI_8/dt = I_7/tau_7 - I_8/T_8
    der(inventory) = (m_7_8 - inventory * inv_T8) / time_scale;
// Table A.2 outflows
    m_8_9 = (1 - f_8_11) * outflow;
    m_8_11 = f_8_11 * outflow;

    annotation(
      Icon(graphics = {
        Rectangle(fillColor = {255, 165, 0}, fillPattern = FillPattern.Solid, extent = {{-100, 100}, {100, -100}}),
        Text(origin = {0, 0}, extent = {{-80, 60}, {80, -60}}, textString = "8: FCU", fontName = "Arial")
      }));
  end FCU;

  // ===========================================================================
  // Component 9: Isotope Separation System (ISS) - Equation (A.9) & Table A.2
  // ===========================================================================
  model ISS "Component 9: Isotope Separation System (Eq. A.9)"
    outer parameter Real time_scale;
    Real inventory(unit = "g", start = 0, fixed = true) "Tritium inventory I_9 (I_9(0) = 0 per Eq. A.13)";
    Real outflow(unit = "g/h") "Total outflow I_9 / tau_9";

    parameter Real tau_9(unit = "h") = Baseline.tau_9 "Processing time tau_9";
    parameter Real lambda_decay(unit = "1/h") = Baseline.lambda_decay "Decay constant lambda";
    parameter Real epsilon_9(unit = "1") = Baseline.eps_nom "Non-radioactive loss fraction epsilon_9 = 1e-4";
    parameter Real f_9_10(unit = "1") = Baseline.f_9_10 "Fraction of outflow to EDS/WDS (f_{9-10})";
    protected
    parameter Real inv_T9(unit = "1/h") = (1 + epsilon_9) / tau_9 + lambda_decay "1 / T_9 per Eq. (A.13)";

  public
    Modelica.Blocks.Interfaces.RealInput m_8_9 annotation(
      Placement(transformation(origin = {-120, 60}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {110, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
    Modelica.Blocks.Interfaces.RealInput m_10_9 annotation(
      Placement(transformation(origin = {-120, 20}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {-40, -110}, extent = {{-10, -10}, {10, 10}}, rotation = 90)));
    Modelica.Blocks.Interfaces.RealInput m_2_9 annotation(
      Placement(transformation(origin = {-120, -20}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {-60, 110}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
    Modelica.Blocks.Interfaces.RealInput m_6_9 annotation(
      Placement(transformation(origin = {-120, -60}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {110, -60}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));

    Modelica.Blocks.Interfaces.RealOutput m_9_10 annotation(
      Placement(transformation(origin = {110, -40}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {40, -110}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
    Modelica.Blocks.Interfaces.RealOutput m_9_11 annotation(
      Placement(transformation(origin = {110, 40}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {40, 110}, extent = {{-10, -10}, {10, 10}}, rotation = 90)));

  equation
    outflow = inventory / tau_9;
// Eq. (A.9): dI_9/dt = (1 - f_{8-11})*(I_8/tau_8) + I_10/tau_10 + eta_2*(I_2/tau_2) + eta_6*(I_6/tau_6) - I_9/T_9
    der(inventory) = (m_8_9 + m_10_9 + m_2_9 + m_6_9 - inventory * inv_T9) / time_scale;
// Table A.2 outflows
    m_9_10 = f_9_10 * outflow;
    m_9_11 = (1 - f_9_10) * outflow;

    annotation(
      Icon(graphics = {
        Rectangle(fillColor = {220, 220, 220}, fillPattern = FillPattern.Solid, extent = {{-100, 100}, {100, -100}}),
        Text(origin = {0, 0}, extent = {{-80, 60}, {80, -60}}, textString = "9: ISS", fontName = "Arial")
      }));
  end ISS;

  // ===========================================================================
  // Component 10: Exhaust & Water Detritiation System (EDS/WDS) - Eq. (A.10)
  // ===========================================================================
  model EDS_WDS "Component 10: Exhaust and Water Detritiation System (Eq. A.10)"
    outer parameter Real time_scale;
    Real inventory(unit = "g", start = 0, fixed = true) "Tritium inventory I_10 (I_10(0) = 0 per Eq. A.13)";
    Real outflow(unit = "g/h") "Total outflow I_10 / tau_10";

    parameter Real tau_10(unit = "h") = Baseline.tau_10 "Processing time tau_10";
    parameter Real lambda_decay(unit = "1/h") = Baseline.lambda_decay "Decay constant lambda";
    parameter Real epsilon_10(unit = "1") = Baseline.eps_nom "Non-radioactive loss fraction epsilon_10 = 1e-4";
    protected
    parameter Real inv_T10(unit = "1/h") = (1 + epsilon_10) / tau_10 + lambda_decay "1 / T_10 per Eq. (A.13)";

  public
    Modelica.Blocks.Interfaces.RealInput m_5_10 annotation(
      Placement(transformation(origin = {-120, 40}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {110, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
    Modelica.Blocks.Interfaces.RealInput m_9_10 annotation(
      Placement(transformation(origin = {-120, -40}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {40, 110}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
    Modelica.Blocks.Interfaces.RealOutput m_10_9 annotation(
      Placement(transformation(origin = {110, 0}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {-40, 110}, extent = {{-10, -10}, {10, 10}}, rotation = 90)));

  equation
    outflow = inventory / tau_10;
// Eq. (A.10): dI_10/dt = f_{5-10}*(I_5/tau_5) + f_{9-10}*(I_9/tau_9) - I_10/T_10
    der(inventory) = (m_5_10 + m_9_10 - inventory * inv_T10) / time_scale;

    m_10_9 = outflow;

    annotation(
      Icon(graphics = {
        Rectangle(fillColor = {144, 238, 144}, fillPattern = FillPattern.Solid, extent = {{-100, 100}, {100, -100}}),
        Text(origin = {0, 0}, extent = {{-80, 60}, {80, -60}}, textString = "10: EDS/WDS", fontName = "Arial")
      }));
  end EDS_WDS;

  // ===========================================================================
  // Component 11: Storage and Management - Equation (A.11) & Table A.2
  // ===========================================================================
  model Storage "Component 11: Storage and Management (Eq. A.11)"
    outer parameter Real time_scale;
    parameter Real I_11_0(unit = "g") = 11300.0 "Initial tritium start-up inventory I_11^0 (I_S^0, Eq. A.13)";
    Real inventory(unit = "g", start = I_11_0, fixed = true) "Tritium inventory I_11";

    parameter Real lambda_decay(unit = "1/h") = Baseline.lambda_decay "Decay constant lambda";
    parameter Real epsilon_11(unit = "1") = Baseline.eps_zero "Non-radioactive loss fraction epsilon_11 = 0";

// --- Section 3.5 Boundary Condition Parameters & Trackers (Eqs. 3.8 - 3.10) ---
    parameter Real P_fus(unit = "MW") = Baseline.Power "Fusion power (MW)";
    parameter Real f_b(unit = "1") = Baseline.f_b "Tritium burn fraction in plasma (f_b)";
    parameter Real eta_f(unit = "1") = Baseline.eta_f "Fueling efficiency (eta_f)";
    parameter Real t_r(unit = "h") = Baseline.t_r "Reserve time t_r (h)";
    parameter Real q_fail(unit = "1") = Baseline.q_fail "Fraction of fuel cycle failing q";
    parameter Real t_d(unit = "h") = Baseline.t_d "Doubling time t_d (h)";

    parameter Real N_dot_nom(unit = "g/h") = Baseline.N_dot_burn_3GW * (P_fus / 3000.0) "Nominal tritium burning rate (g/h)";
    Real I_reserve_req(unit = "g")
      "Required reserve inventory I_r = (N_dot^- / (eta_f * f_b)) * t_r * q (Eq. 3.9)";
    parameter Real I_doubling_target(unit = "g") = 2.0 * I_11_0
      "Target storage inventory at doubling time t_d: I_S(t_d) = 2 * I_S^0 (Eq. 3.10)";

    Modelica.Blocks.Interfaces.RealInput m_8_11 annotation(
      Placement(transformation(origin = {-120, 40}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {0, -110}, extent = {{-10, -10}, {10, 10}}, rotation = 90)));
    Modelica.Blocks.Interfaces.RealInput m_9_11 annotation(
      Placement(transformation(origin = {-120, -40}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {-60, -110}, extent = {{-10, -10}, {10, 10}}, rotation = 90)));
    Modelica.Blocks.Interfaces.RealInput m_11_12_req annotation(
      Placement(transformation(origin = {120, -40}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {110, -40}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
    Modelica.Blocks.Interfaces.RealOutput m_11_12 annotation(
      Placement(transformation(origin = {110, 40}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {110, 40}, extent = {{-10, -10}, {10, 10}})));

  equation
    I_reserve_req = (N_dot_nom / (eta_f * f_b)) * t_r * q_fail;
    m_11_12 = m_11_12_req;
// Eq. (A.11): dI_11/dt = f_{8-11}*(I_8/tau_8) + (1 - f_{9-10})*(I_9/tau_9) - N_dot^-/(eta_f*f_b) - lambda*I_11
    der(inventory) = (m_8_11 + m_9_11 - m_11_12 - lambda_decay * inventory) / time_scale;

    annotation(
      Icon(graphics = {
        Rectangle(fillColor = {255, 215, 0}, fillPattern = FillPattern.Solid, extent = {{-100, 100}, {100, -100}}),
        Text(origin = {0, 0}, extent = {{-80, 60}, {80, -60}}, textString = "11: Storage", fontName = "Arial")
      }));
  end Storage;

  // ===========================================================================
  // Component 12: Fueling System (FS) - Equation (A.12) & Table A.2
  // ===========================================================================
  model FS "Component 12: Fueling System (Eq. A.12: dI_12/dt = 0, not simulated)"
    Real inventory(unit = "g") = 0.0 "I_12 = 0 (Eq. A.12: not simulated separately; included in IFC t_p)";

    Modelica.Blocks.Interfaces.RealInput m_12_p_req annotation(
      Placement(transformation(origin = {120, -40}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {110, -40}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
    Modelica.Blocks.Interfaces.RealInput m_11_12 annotation(
      Placement(transformation(origin = {-120, 40}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {-110, 40}, extent = {{-10, -10}, {10, 10}})));
    Modelica.Blocks.Interfaces.RealOutput m_11_12_req annotation(
      Placement(transformation(origin = {-110, -40}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {-110, -40}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
    Modelica.Blocks.Interfaces.RealOutput m_12_p annotation(
      Placement(transformation(origin = {110, 40}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {110, 40}, extent = {{-10, -10}, {10, 10}})));

  equation
// Table A.2 Component 12: m_{11-12} = N_dot^- / (eta_f * f_b), m_{12-p} = N_dot^- / (eta_f * f_b)
    m_11_12_req = m_12_p_req;
    m_12_p = m_11_12;

    annotation(
      Icon(graphics = {
        Rectangle(fillColor = {173, 216, 230}, fillPattern = FillPattern.Solid, extent = {{-100, 100}, {100, -100}}),
        Text(origin = {0, 0}, extent = {{-80, 60}, {80, -60}}, textString = "12: Fueling", fontName = "Arial")
      }));
  end FS;

  // ===========================================================================
  // Plasma Core & SOL Node - Figure A.1, Equations (3.3)-(3.5), Table A.1 & A.2
  // ===========================================================================
  model Plasma "Plasma Core & SOL Flow Splitter (Fig. A.1 & Eqs. 3.5, A.3, A.4, A.7)"
    Real inventory(unit = "g") = 0.0 "Zero-residence node in Appendix A";

    parameter Real f_b(unit = "1") = Baseline.f_b "Tritium burn fraction f_b";
    parameter Real eta_f(unit = "1") = Baseline.eta_f "Fueling efficiency eta_f";
    parameter Real f_p_3(unit = "1") = Baseline.f_p_3 "Fraction of injected T to First Wall (f_{p-3})";
    parameter Real f_p_4(unit = "1") = Baseline.f_p_4 "Fraction of injected T to Divertor (f_{p-4})";

    Modelica.Blocks.Interfaces.RealInput N_dot_burn annotation(
      Placement(transformation(origin = {-120, 60}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {0, 110}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
    Modelica.Blocks.Interfaces.RealInput m_12_p annotation(
      Placement(transformation(origin = {-120, 0}, extent = {{-20, -20}, {20, 20}}),
                iconTransformation(origin = {-110, 40}, extent = {{-10, -10}, {10, 10}})));
    Modelica.Blocks.Interfaces.RealOutput m_12_p_req annotation(
      Placement(transformation(origin = {-110, -60}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {-110, -40}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));

    Modelica.Blocks.Interfaces.RealOutput m_p_3 annotation(
      Placement(transformation(origin = {110, 60}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {110, 40}, extent = {{-10, -10}, {10, 10}})));
    Modelica.Blocks.Interfaces.RealOutput m_p_4 annotation(
      Placement(transformation(origin = {110, 0}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {110, -40}, extent = {{-10, -10}, {10, 10}})));
    Modelica.Blocks.Interfaces.RealOutput m_p_7 annotation(
      Placement(transformation(origin = {110, -60}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {0, -110}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));

  equation
// Eq. (3.5): T_dot_i = N_dot^- / (eta_f * f_b)
    m_12_p_req = N_dot_burn / (eta_f * f_b);
// Table A.1 & Table A.2 exact plasma exhaust / implantation splits
    m_p_3 = f_p_3 * m_12_p;
    m_p_4 = f_p_4 * m_12_p;
    m_p_7 = (1.0 - eta_f * f_b - f_p_3 - f_p_4) * m_12_p;

    annotation(
      Icon(graphics = {
        Ellipse(fillColor = {255, 182, 193}, fillPattern = FillPattern.Solid, extent = {{-100, 100}, {100, -100}}),
        Text(origin = {0, 0}, extent = {{-80, 60}, {80, -60}}, textString = "DT Plasma", fontName = "Arial")
      }));
  end Plasma;

  // ===========================================================================
  // Availability Factor Switch Operation - Section 3.6, Equation (3.11)
  // ===========================================================================
  block AvailabilitySwitch
    "Reactor Availability Factor (AF) Switch Operation based on MTBF and MTTR (Sec. 3.6, Eq. 3.11)"
    outer parameter Real time_scale;
    parameter Real P_fus(unit = "MW") = Baseline.Power "Fusion power (MW)";
    parameter Real N_dot_nom(unit = "g/h") = Baseline.N_dot_burn_3GW * (P_fus / 3000.0) "Nominal tritium burn rate when plasma is ON (g/h)";
    parameter Real AF(unit = "1", min = 1e-6, max = 1.0) = Baseline.AF "Availability factor AF = MTBF / (MTBF + MTTR) (Eq. 3.11)";
    parameter Real MTTR(unit = "h") = 48.0 "Mean Time To Repair (plasma OFF duration, h)";
    parameter Real MTBF(unit = "h") = if AF >= 1.0 then 1e12 else MTTR * AF / (1.0 - AF) "Mean Time Between Failures (plasma ON duration, h)";
    parameter Real startTime(unit = "h") = 0.0 "Start time of operation (h)";

    Modelica.Blocks.Interfaces.RealOutput y1 annotation(
      Placement(transformation(origin = {110, 30}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {-110, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
    Modelica.Blocks.Interfaces.RealOutput y2 annotation(
      Placement(transformation(origin = {110, -30}, extent = {{-10, -10}, {10, 10}}),
                iconTransformation(origin = {110, 0}, extent = {{-10, -10}, {10, 10}})));

  protected
    Real cycle_period(unit = "s") = (MTBF + MTTR) * time_scale;
    Real on_duration(unit = "s") = MTBF * time_scale;

  equation
    y1 = if time < startTime * time_scale then 0.0
         else if AF >= 1.0 then N_dot_nom
         else if mod(time - startTime * time_scale, cycle_period) <= on_duration then N_dot_nom
         else 0.0;
    y2 = y1;

    annotation(
      Icon(graphics = {
        Rectangle(fillColor = {240, 240, 240}, fillPattern = FillPattern.Solid, extent = {{-100, 100}, {100, -100}}),
        Text(origin = {0, 0}, extent = {{-80, 60}, {80, -60}}, textString = "AF Switch\n(MTBF/MTTR)", fontName = "Arial")
      }));
  end AvailabilitySwitch;

  // ===========================================================================
  // Top-Level System Model: 12-Component Fuel Cycle + Boundary Conditions
  // ===========================================================================
  model Cycle
    "Complete 12-Compartment Fuel Cycle Dynamic Model & Boundary Condition Evaluators (Abdou 2021)"
    inner parameter Real time_scale = 3600.0 "Time-base factor: 1 = hour-based axis, 3600 = second-based axis";

// --- Key Physics & Technology Parameters ---
    parameter Real P_fus(unit = "MW") = Baseline.Power "Fusion power (MW)";
    parameter Real f_b(unit = "1") = Baseline.f_b "Tritium burn fraction in plasma (f_b)";
    parameter Real eta_f(unit = "1") = Baseline.eta_f "Fueling efficiency (eta_f)";
    parameter Real Lambda(unit = "1") = Baseline.Lambda "Required TBR (Lambda in Eq. A.1)";
    parameter Real AF(unit = "1") = Baseline.AF "Reactor availability factor (AF in Eq. 3.11)";
    parameter Real f_DIR(unit = "1") = Baseline.f_8_11 "Direct Internal Recycling fraction (f_{8-11})";
    parameter Real t_r(unit = "h") = Baseline.t_r "Reserve time t_r (h)";
    parameter Real q_fail(unit = "1") = Baseline.q_fail "Fraction of fuel cycle failing q";
    parameter Real t_d(unit = "h") = Baseline.t_d "Doubling time t_d (h)";
    parameter Real I_S_0(unit = "g") = 14650.0 "Initial start-up tritium inventory I_11(0) = I_S^0 (g)";

// --- 12 Compartments + Plasma + AF Switch ---
    BZ comp1_BZ(Lambda = Lambda) annotation(
      Placement(transformation(origin = {120, 80}, extent = {{-12, -12}, {12, 12}})));
    TES comp2_TES annotation(
      Placement(transformation(origin = {170, 80}, extent = {{-12, -12}, {12, 12}})));
    FW comp3_FW annotation(
      Placement(transformation(origin = {40, 20}, extent = {{-12, -12}, {12, 12}})));
    DIV comp4_DIV annotation(
      Placement(transformation(origin = {40, -40}, extent = {{-12, -12}, {12, 12}})));
    HX comp5_HX annotation(
      Placement(transformation(origin = {140, -10}, extent = {{-12, -12}, {12, 12}})));
    CPS comp6_CPS annotation(
      Placement(transformation(origin = {140, -70}, extent = {{-12, -12}, {12, 12}})));
    VacuumPump comp7_Pump annotation(
      Placement(transformation(origin = {-50, -80}, extent = {{-12, -12}, {12, 12}})));
    FCU comp8_FCU(f_8_11 = f_DIR) annotation(
      Placement(transformation(origin = {-110, -80}, extent = {{-12, -12}, {12, 12}})));
    ISS comp9_ISS annotation(
      Placement(transformation(origin = {-170, -20}, extent = {{-12, -12}, {12, 12}})));
    EDS_WDS comp10_EDS_WDS annotation(
      Placement(transformation(origin = {-120, -140}, extent = {{-12, -12}, {12, 12}})));
    Storage comp11_Storage(
      I_11_0 = I_S_0,
      P_fus = P_fus,
      f_b = f_b,
      eta_f = eta_f,
      t_r = t_r,
      q_fail = q_fail,
      t_d = t_d) annotation(
      Placement(transformation(origin = {-120, 80}, extent = {{-12, -12}, {12, 12}})));
    FS comp12_FS annotation(
      Placement(transformation(origin = {-60, 80}, extent = {{-12, -12}, {12, 12}})));
    Plasma plasma(f_b = f_b, eta_f = eta_f) annotation(
      Placement(transformation(origin = {-30, 0}, extent = {{-14, -14}, {14, 14}})));
    AvailabilitySwitch af_switch(P_fus = P_fus, AF = AF) annotation(
      Placement(transformation(origin = {20, 125}, extent = {{-12, -12}, {12, 12}})));

// --- Dynamic Mass Closure Tracking ---
    Real plant_total_inv(unit = "g") "Total tritium inventory across all 12 compartments";
    Real cumulative_breed(unit = "g", start = 0, fixed = true) "Integrated tritium bred in BZ";
    Real cumulative_burn(unit = "g", start = 0, fixed = true) "Integrated tritium burned in plasma";
    Real cumulative_decay(unit = "g", start = 0, fixed = true) "Integrated radioactive decay loss";
    Real cumulative_loss(unit = "g", start = 0, fixed = true) "Integrated non-radioactive loss (sum of epsilon_i * I_i / tau_i)";
    Real loss_rate(unit = "g/h") "Instantaneous non-radioactive loss rate";
    Real plant_mass_residual(unit = "g") "Global mass balance closure residual R_plant(t)";
    Real I_reserve_req(unit = "g") "Required reserve inventory I_r = (N_dot^- / (eta_f * f_b)) * t_r * q (Eq. 3.9)";

  equation
// --- Connections for Outer Fuel Cycle (OFC) ---
    connect(af_switch.y1, plasma.N_dot_burn);
    connect(af_switch.y2, comp1_BZ.N_dot_burn);

    connect(comp1_BZ.m_1_2, comp2_TES.m_1_2);
    connect(comp2_TES.m_2_1, comp1_BZ.m_2_1);
    connect(comp1_BZ.m_1_5, comp5_HX.m_1_5);
    connect(comp2_TES.m_2_9, comp9_ISS.m_2_9);

    connect(plasma.m_p_3, comp3_FW.m_p_3);
    connect(plasma.m_p_4, comp4_DIV.m_p_4);
    connect(comp3_FW.m_3_5, comp5_HX.m_3_5);
    connect(comp4_DIV.m_4_5, comp5_HX.m_4_5);

    connect(comp5_HX.m_5_3, comp3_FW.m_5_3);
    connect(comp5_HX.m_5_4, comp4_DIV.m_5_4);
    connect(comp5_HX.m_5_6, comp6_CPS.m_5_6);
    connect(comp5_HX.m_5_10, comp10_EDS_WDS.m_5_10);

    connect(comp6_CPS.m_6_3, comp3_FW.m_6_3);
    connect(comp6_CPS.m_6_4, comp4_DIV.m_6_4);
    connect(comp6_CPS.m_6_9, comp9_ISS.m_6_9);
// --- Connections for Inner Fuel Cycle (IFC) ---
    connect(plasma.m_p_7, comp7_Pump.m_p_7);
    connect(comp7_Pump.m_7_8, comp8_FCU.m_7_8);
    connect(comp8_FCU.m_8_9, comp9_ISS.m_8_9);
    connect(comp8_FCU.m_8_11, comp11_Storage.m_8_11);

    connect(comp9_ISS.m_9_10, comp10_EDS_WDS.m_9_10);
    connect(comp10_EDS_WDS.m_10_9, comp9_ISS.m_10_9);
    connect(comp9_ISS.m_9_11, comp11_Storage.m_9_11);

    connect(comp11_Storage.m_11_12, comp12_FS.m_11_12);
    connect(comp12_FS.m_11_12_req, comp11_Storage.m_11_12_req);
    connect(comp12_FS.m_12_p, plasma.m_12_p);
    connect(plasma.m_12_p_req, comp12_FS.m_12_p_req);
// --- Exact Global Mass Balance Verification ---
    plant_total_inv = comp1_BZ.inventory + comp2_TES.inventory + comp3_FW.inventory
                    + comp4_DIV.inventory + comp5_HX.inventory + comp6_CPS.inventory
                    + comp7_Pump.inventory + comp8_FCU.inventory + comp9_ISS.inventory
                    + comp10_EDS_WDS.inventory + comp11_Storage.inventory + comp12_FS.inventory;

    loss_rate = comp1_BZ.epsilon_1 * comp1_BZ.outflow
              + comp2_TES.epsilon_2 * comp2_TES.outflow
              + comp3_FW.epsilon_3 * comp3_FW.outflow
              + comp4_DIV.epsilon_4 * comp4_DIV.outflow
              + comp5_HX.epsilon_5 * comp5_HX.outflow
              + comp6_CPS.epsilon_6 * comp6_CPS.outflow
              + comp7_Pump.epsilon_7 * comp7_Pump.outflow
              + comp8_FCU.epsilon_8 * comp8_FCU.outflow
              + comp9_ISS.epsilon_9 * comp9_ISS.outflow
              + comp10_EDS_WDS.epsilon_10 * comp10_EDS_WDS.outflow;

    der(cumulative_breed) = comp1_BZ.S_1 / time_scale;
    der(cumulative_burn) = af_switch.y1 / time_scale;
    der(cumulative_decay) = (Baseline.lambda_decay * plant_total_inv) / time_scale;
    der(cumulative_loss) = loss_rate / time_scale;

    plant_mass_residual = abs(plant_total_inv - (I_S_0 + cumulative_breed - cumulative_burn - cumulative_decay - cumulative_loss));
    I_reserve_req = comp11_Storage.I_reserve_req;

    annotation(
      Diagram(coordinateSystem(extent = {{-200, 150}, {200, -170}})),
      experiment(StartTime = 0, StopTime = 157788000, Tolerance = 1e-6));
  end Cycle;

  annotation(uses(Modelica(version = "4.0.0")));
end Abdou2021;
