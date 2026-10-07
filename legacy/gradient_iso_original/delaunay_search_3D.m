
function [Result_vec] = delaunay_search_3D(arg1, arg2, arg3, arg4, ...
    arg5, arg6, T)
% INPUTS
%   arg1   n x m matrix with measured values that should be interpolated
%   n: amount of measurements performed
%   m: amount of different input variables, the first three columns are the  
%   x, y, z values of the DoE plane, the thrid column contains the variable 
%   where that defines plane intersections (equipotential lines), all 
%   additional columns are measured values that should be interpolated 
%   with respect to the calculated equipotential lines (amount can vary)

%   arg2   a of parameter hyperplane equation, default = 0
%   arg3   b of parameter hyperplane equation, default = 0
%   arg4   c of parameter hyperplane equation, default = 0
%   arg5   d of parameter hyperplane equation, default = 1
%   arg6   e of parameter hyperplane equation, default = value of 
%   equipotential line
%   T:     Delaunay Matrix


%% Check for Validity
validity_range = 3;


% Define Points of Hypersimplex
P1_matrix = [arg1(T(:,1),1) arg1(T(:,1),2) arg1(T(:,1),3) arg1(T(:,1),4)];
P2_matrix = [arg1(T(:,2),1) arg1(T(:,2),2) arg1(T(:,2),3) arg1(T(:,2),4)];
P3_matrix = [arg1(T(:,3),1) arg1(T(:,3),2) arg1(T(:,3),3) arg1(T(:,3),4)];
P4_matrix = [arg1(T(:,4),1) arg1(T(:,4),2) arg1(T(:,4),3) arg1(T(:,4),4)];

% Define Edges of Hypersimplex

% Hypervector 1: P1 --> P2
Vector_1_2 = P2_matrix - P1_matrix;
% Hypervector 2: P2 --> P3
Vector_2_3 = P3_matrix - P2_matrix;
% Hypervector 3: P3 --> P1
Vector_3_1 = P1_matrix - P3_matrix;
% Hypervector 4: P4 --> P1
Vector_4_1 = P1_matrix - P4_matrix;
% Hypervector 5: P4 --> P2
Vector_4_2 = P2_matrix - P4_matrix;
% Hypervector 6: P4 --> P3
Vector_4_3 = P3_matrix - P4_matrix;

% Check if Delaunay Triangulation yields consistent Hypersimplex
norm_vector_1_2 = sqrt(Vector_1_2(:,1).^2 + Vector_1_2(:,2).^2 + Vector_1_2(:,3).^2);
norm_vector_2_3 = sqrt(Vector_2_3(:,1).^2 + Vector_2_3(:,2).^2 + Vector_2_3(:,3).^2);
norm_vector_3_1 = sqrt(Vector_3_1(:,1).^2 + Vector_3_1(:,2).^2 + Vector_3_1(:,3).^2);
norm_vector_4_1 = sqrt(Vector_4_1(:,1).^2 + Vector_4_1(:,2).^2 + Vector_4_1(:,3).^2);
norm_vector_4_2 = sqrt(Vector_4_2(:,1).^2 + Vector_4_2(:,2).^2 + Vector_4_2(:,3).^2);
norm_vector_4_3 = sqrt(Vector_4_3(:,1).^2 + Vector_4_3(:,2).^2 + Vector_4_3(:,3).^2);

index_norm_vector = find(norm_vector_1_2 >...
    validity_range * mean(norm_vector_1_2));
index_norm_vector = [index_norm_vector; ...
    find(norm_vector_2_3 > validity_range * mean(norm_vector_2_3))];
index_norm_vector = [index_norm_vector; ...
    find(norm_vector_3_1 > validity_range * mean(norm_vector_3_1))];
index_norm_vector = [index_norm_vector; ...
    find(norm_vector_4_1 > validity_range * mean(norm_vector_4_1))];
index_norm_vector = [index_norm_vector; ...
    find(norm_vector_4_2 > validity_range * mean(norm_vector_4_2))];
index_norm_vector = [index_norm_vector; ...
    find(norm_vector_4_3 > validity_range * mean(norm_vector_4_3))];

index_norm_vector = unique(index_norm_vector);

% Delete Hypersimplex that are not valid in all data points
T(index_norm_vector,:) = []; 


%% Init
% Length of T
amount_tri = length(T(:,1));

% plane form ax + by + cz = d
a = arg2;
b = arg3;
c = arg4;
d = arg5;
e = arg6;

a_vector = arg2 * ones(amount_tri,1);
b_vector = arg3 * ones(amount_tri,1);
c_vector = arg4 * ones(amount_tri,1);
d_vector = arg5 * ones(amount_tri,1);
e_vector = arg6 * ones(amount_tri,1);


%% Start Calculation

% Define Points of Hypersimplex
P1_matrix = [arg1(T(:,1),1) arg1(T(:,1),2) arg1(T(:,1),3) arg1(T(:,1),4)];
P2_matrix = [arg1(T(:,2),1) arg1(T(:,2),2) arg1(T(:,2),3) arg1(T(:,2),4)];
P3_matrix = [arg1(T(:,3),1) arg1(T(:,3),2) arg1(T(:,3),3) arg1(T(:,3),4)];
P4_matrix = [arg1(T(:,4),1) arg1(T(:,4),2) arg1(T(:,4),3) arg1(T(:,4),4)];

% Define Edges of Hypersimplex

% Hypervector 1: P1 --> P2
Vector_1_2 = P2_matrix - P1_matrix;
% Hypervector 2: P2 --> P3
Vector_2_3 = P3_matrix - P2_matrix;
% Hypervector 3: P3 --> P1
Vector_3_1 = P1_matrix - P3_matrix;
% Hypervector 4: P4 --> P1
Vector_4_1 = P1_matrix - P4_matrix;
% Hypervector 5: P4 --> P2
Vector_4_2 = P2_matrix - P4_matrix;
% Hypervector 6: P4 --> P3
Vector_4_3 = P3_matrix - P4_matrix;


% Aux_P12: Half Vector 1 + P_1
Aux_P_12 = P1_matrix + 0.5 * Vector_1_2;
% Aux_P23: Half Vector 2 + P_2
Aux_P_23 = P2_matrix + 0.5 * Vector_2_3;
% Aux_P31: Half Vector 3 + P_3
Aux_P_31 = P3_matrix + 0.5 * Vector_3_1;
% Aux_P14: Half Vector 4 + P_1
Aux_P_14 = P4_matrix + 0.5 * Vector_4_1;
% Aux_P24: Half Vector 4 + P_2
Aux_P_24 = P4_matrix + 0.5 * Vector_4_1;
% Aux_P34: Half Vector 4 + P_3
Aux_P_34 = P4_matrix + 0.5 * Vector_4_1;


% Define additional hypervectors - Aux Points to Edges
Aux_Vector_12_3 = P3_matrix - Aux_P_12;
Aux_Vector_12_4 = P4_matrix - Aux_P_12;
Aux_Vector_23_1 = P1_matrix - Aux_P_23;
Aux_Vector_23_4 = P4_matrix - Aux_P_23;
Aux_Vector_31_2 = P2_matrix - Aux_P_31;
Aux_Vector_31_4 = P4_matrix - Aux_P_31;
Aux_Vector_14_3 = P3_matrix - Aux_P_14;
Aux_Vector_14_2 = P2_matrix - Aux_P_14;
Aux_Vector_24_1 = P1_matrix - Aux_P_24;
Aux_Vector_24_3 = P3_matrix - Aux_P_24;
Aux_Vector_34_1 = P1_matrix - Aux_P_34;
Aux_Vector_34_2 = P2_matrix - Aux_P_34;

% Aux Points to Aux Points
Aux_Vector_12_23 =  Aux_P_23 - Aux_P_12;
Aux_Vector_23_31 =  Aux_P_31 - Aux_P_23;
Aux_Vector_31_12 =  Aux_P_12 - Aux_P_31;
Aux_Vector_12_14 =  Aux_P_14 - Aux_P_12;
Aux_Vector_12_24 =  Aux_P_24 - Aux_P_12;
Aux_Vector_12_34 =  Aux_P_34 - Aux_P_12;
Aux_Vector_23_14 =  Aux_P_14 - Aux_P_23;
Aux_Vector_23_24 =  Aux_P_24 - Aux_P_23;
Aux_Vector_23_34 =  Aux_P_34 - Aux_P_23;
Aux_Vector_31_14 =  Aux_P_14 - Aux_P_31;
Aux_Vector_31_24 =  Aux_P_24 - Aux_P_31;
Aux_Vector_31_34 =  Aux_P_34 - Aux_P_31;

lambda_matrix(:,1) = (e_vector - (P1_matrix(:,1).* a_vector + ...
    P1_matrix(:,2).* b_vector + P1_matrix(:,3).* c_vector + ...
    P1_matrix(:,4).* d_vector)) ./ (...
    Vector_1_2(:,1).* a_vector + ...
    Vector_1_2(:,2).* b_vector + Vector_1_2(:,3).* c_vector + ...
    Vector_1_2(:,4).* d_vector);

lambda_matrix(:,2) = (e_vector - (P2_matrix(:,1).* a_vector + ...
    P2_matrix(:,2).* b_vector + P2_matrix(:,3).* c_vector + ...
    P2_matrix(:,4).* d_vector)) ./ (...
    Vector_2_3(:,1).* a_vector + ...
    Vector_2_3(:,2).* b_vector + Vector_2_3(:,3).* c_vector + ...
    Vector_2_3(:,4).* d_vector);

lambda_matrix(:,3) = (e_vector - (P3_matrix(:,1).* a_vector + ...
    P3_matrix(:,2).* b_vector + P3_matrix(:,3).* c_vector + ...
    P3_matrix(:,4).* d_vector)) ./ (...
    Vector_3_1(:,1).* a_vector + ...
    Vector_3_1(:,2).* b_vector + Vector_3_1(:,3).* c_vector + ...
    Vector_3_1(:,4).* d_vector);

lambda_matrix(:,4) = (e_vector - (P4_matrix(:,1).* a_vector + ...
    P4_matrix(:,2).* b_vector + P4_matrix(:,3).* c_vector + ...
    P4_matrix(:,4).* d_vector)) ./ (...
    Vector_4_1(:,1).* a_vector + ...
    Vector_4_1(:,2).* b_vector + Vector_4_1(:,3).* c_vector + ...
    Vector_4_1(:,4).* d_vector);

lambda_matrix(:,5) = (e_vector - (Aux_P_12(:,1).* a_vector + ...
    Aux_P_12(:,2).* b_vector + Aux_P_12(:,3).* c_vector + ...
    Aux_P_12(:,4).* d_vector)) ./ (...
    Aux_Vector_12_3(:,1).* a_vector + ...
    Aux_Vector_12_3(:,2).* b_vector + Aux_Vector_12_3(:,3).* c_vector + ...
    Aux_Vector_12_3(:,4).* d_vector);

lambda_matrix(:,6) = (e_vector - (Aux_P_12(:,1).* a_vector + ...
    Aux_P_12(:,2).* b_vector + Aux_P_12(:,3).* c_vector + ...
    Aux_P_12(:,4).* d_vector)) ./ (...
    Aux_Vector_12_4(:,1).* a_vector + ...
    Aux_Vector_12_4(:,2).* b_vector + Aux_Vector_12_4(:,3).* c_vector + ...
    Aux_Vector_12_4(:,4).* d_vector);

lambda_matrix(:,7) = (e_vector - (Aux_P_23(:,1).* a_vector + ...
    Aux_P_23(:,2).* b_vector + Aux_P_23(:,3).* c_vector + ...
    Aux_P_23(:,4).* d_vector)) ./ (...
    Aux_Vector_23_1(:,1).* a_vector + ...
    Aux_Vector_23_1(:,2).* b_vector + Aux_Vector_23_1(:,3).* c_vector + ...
    Aux_Vector_23_1(:,4).* d_vector);

lambda_matrix(:,8) = (e_vector - (Aux_P_23(:,1).* a_vector + ...
    Aux_P_23(:,2).* b_vector + Aux_P_23(:,3).* c_vector + ...
    Aux_P_23(:,4).* d_vector)) ./ (...
    Aux_Vector_23_4(:,1).* a_vector + ...
    Aux_Vector_23_4(:,2).* b_vector + Aux_Vector_23_4(:,3).* c_vector + ...
    Aux_Vector_23_4(:,4).* d_vector);

lambda_matrix(:,9) = (e_vector - (Aux_P_31(:,1).* a_vector + ...
    Aux_P_31(:,2).* b_vector + Aux_P_31(:,3).* c_vector + ...
    Aux_P_31(:,4).* d_vector)) ./ (...
    Aux_Vector_31_2(:,1).* a_vector + ...
    Aux_Vector_31_2(:,2).* b_vector + Aux_Vector_31_2(:,3).* c_vector + ...
    Aux_Vector_31_2(:,4).* d_vector);

lambda_matrix(:,10) = (e_vector - (Aux_P_31(:,1).* a_vector + ...
    Aux_P_31(:,2).* b_vector + Aux_P_31(:,3).* c_vector + ...
    Aux_P_31(:,4).* d_vector)) ./ (...
    Aux_Vector_31_4(:,1).* a_vector + ...
    Aux_Vector_31_4(:,2).* b_vector + Aux_Vector_31_4(:,3).* c_vector + ...
    Aux_Vector_31_4(:,4).* d_vector);

lambda_matrix(:,11) = (e_vector - (Aux_P_14(:,1).* a_vector + ...
    Aux_P_14(:,2).* b_vector + Aux_P_14(:,3).* c_vector + ...
    Aux_P_14(:,4).* d_vector)) ./ (...
    Aux_Vector_14_3(:,1).* a_vector + ...
    Aux_Vector_14_3(:,2).* b_vector + Aux_Vector_14_3(:,3).* c_vector + ...
    Aux_Vector_14_3(:,4).* d_vector);

lambda_matrix(:,12) = (e_vector - (Aux_P_14(:,1).* a_vector + ...
    Aux_P_14(:,2).* b_vector + Aux_P_14(:,3).* c_vector + ...
    Aux_P_14(:,4).* d_vector)) ./ (...
    Aux_Vector_14_2(:,1).* a_vector + ...
    Aux_Vector_14_2(:,2).* b_vector + Aux_Vector_14_2(:,3).* c_vector + ...
    Aux_Vector_14_2(:,4).* d_vector);

lambda_matrix(:,13) = (e_vector - (Aux_P_24(:,1).* a_vector + ...
    Aux_P_24(:,2).* b_vector + Aux_P_24(:,3).* c_vector + ...
    Aux_P_24(:,4).* d_vector)) ./ (...
    Aux_Vector_24_1(:,1).* a_vector + ...
    Aux_Vector_24_1(:,2).* b_vector + Aux_Vector_24_1(:,3).* c_vector + ...
    Aux_Vector_24_1(:,4).* d_vector);

lambda_matrix(:,14) = (e_vector - (Aux_P_24(:,1).* a_vector + ...
    Aux_P_24(:,2).* b_vector + Aux_P_24(:,3).* c_vector + ...
    Aux_P_24(:,4).* d_vector)) ./ (...
    Aux_Vector_24_3(:,1).* a_vector + ...
    Aux_Vector_24_3(:,2).* b_vector + Aux_Vector_24_3(:,3).* c_vector + ...
    Aux_Vector_24_3(:,4).* d_vector);

lambda_matrix(:,15) = (e_vector - (Aux_P_34(:,1).* a_vector + ...
    Aux_P_34(:,2).* b_vector + Aux_P_34(:,3).* c_vector + ...
    Aux_P_34(:,4).* d_vector)) ./ (...
    Aux_Vector_34_1(:,1).* a_vector + ...
    Aux_Vector_34_1(:,2).* b_vector + Aux_Vector_34_1(:,3).* c_vector + ...
    Aux_Vector_34_1(:,4).* d_vector);

lambda_matrix(:,16) = (e_vector - (Aux_P_34(:,1).* a_vector + ...
    Aux_P_34(:,2).* b_vector + Aux_P_34(:,3).* c_vector + ...
    Aux_P_34(:,4).* d_vector)) ./ (...
    Aux_Vector_34_2(:,1).* a_vector + ...
    Aux_Vector_34_2(:,2).* b_vector + Aux_Vector_34_2(:,3).* c_vector + ...
    Aux_Vector_34_2(:,4).* d_vector);

lambda_matrix(:,17) = (e_vector - (Aux_P_12(:,1).* a_vector + ...
    Aux_P_12(:,2).* b_vector + Aux_P_12(:,3).* c_vector + ...
    Aux_P_12(:,4).* d_vector)) ./ (...
    Aux_Vector_12_23(:,1).* a_vector + ...
    Aux_Vector_12_23(:,2).* b_vector + Aux_Vector_12_23(:,3).* c_vector + ...
    Aux_Vector_12_23(:,4).* d_vector);

lambda_matrix(:,18) = (e_vector - (Aux_P_23(:,1).* a_vector + ...
    Aux_P_23(:,2).* b_vector + Aux_P_23(:,3).* c_vector + ...
    Aux_P_23(:,4).* d_vector)) ./ (...
    Aux_Vector_23_31(:,1).* a_vector + ...
    Aux_Vector_23_31(:,2).* b_vector + Aux_Vector_23_31(:,3).* c_vector + ...
    Aux_Vector_23_31(:,4).* d_vector);

lambda_matrix(:,19) = (e_vector - (Aux_P_31(:,1).* a_vector + ...
    Aux_P_31(:,2).* b_vector + Aux_P_31(:,3).* c_vector + ...
    Aux_P_31(:,4).* d_vector)) ./ (...
    Aux_Vector_31_12(:,1).* a_vector + ...
    Aux_Vector_31_12(:,2).* b_vector + Aux_Vector_31_12(:,3).* c_vector + ...
    Aux_Vector_31_12(:,4).* d_vector);

lambda_matrix(:,20) = (e_vector - (Aux_P_12(:,1).* a_vector + ...
    Aux_P_12(:,2).* b_vector + Aux_P_12(:,3).* c_vector + ...
    Aux_P_12(:,4).* d_vector)) ./ (...
    Aux_Vector_12_14(:,1).* a_vector + ...
    Aux_Vector_12_14(:,2).* b_vector + Aux_Vector_12_14(:,3).* c_vector + ...
    Aux_Vector_12_14(:,4).* d_vector);

lambda_matrix(:,21) = (e_vector - (Aux_P_12(:,1).* a_vector + ...
    Aux_P_12(:,2).* b_vector + Aux_P_12(:,3).* c_vector + ...
    Aux_P_12(:,4).* d_vector)) ./ (...
    Aux_Vector_12_24(:,1).* a_vector + ...
    Aux_Vector_12_24(:,2).* b_vector + Aux_Vector_12_24(:,3).* c_vector + ...
    Aux_Vector_12_24(:,4).* d_vector);

lambda_matrix(:,22) = (e_vector - (Aux_P_12(:,1).* a_vector + ...
    Aux_P_12(:,2).* b_vector + Aux_P_12(:,3).* c_vector + ...
    Aux_P_12(:,4).* d_vector)) ./ (...
    Aux_Vector_12_34(:,1).* a_vector + ...
    Aux_Vector_12_34(:,2).* b_vector + Aux_Vector_12_34(:,3).* c_vector + ...
    Aux_Vector_12_34(:,4).* d_vector);

lambda_matrix(:,23) = (e_vector - (Aux_P_23(:,1).* a_vector + ...
    Aux_P_23(:,2).* b_vector + Aux_P_23(:,3).* c_vector + ...
    Aux_P_23(:,4).* d_vector)) ./ (...
    Aux_Vector_23_14(:,1).* a_vector + ...
    Aux_Vector_23_14(:,2).* b_vector + Aux_Vector_23_14(:,3).* c_vector + ...
    Aux_Vector_23_14(:,4).* d_vector);

lambda_matrix(:,24) = (e_vector - (Aux_P_23(:,1).* a_vector + ...
    Aux_P_23(:,2).* b_vector + Aux_P_23(:,3).* c_vector + ...
    Aux_P_23(:,4).* d_vector)) ./ (...
    Aux_Vector_23_24(:,1).* a_vector + ...
    Aux_Vector_23_24(:,2).* b_vector + Aux_Vector_23_24(:,3).* c_vector + ...
    Aux_Vector_23_24(:,4).* d_vector);

lambda_matrix(:,25) = (e_vector - (Aux_P_23(:,1).* a_vector + ...
    Aux_P_23(:,2).* b_vector + Aux_P_23(:,3).* c_vector + ...
    Aux_P_23(:,4).* d_vector)) ./ (...
    Aux_Vector_23_34(:,1).* a_vector + ...
    Aux_Vector_23_34(:,2).* b_vector + Aux_Vector_23_34(:,3).* c_vector + ...
    Aux_Vector_23_34(:,4).* d_vector);

lambda_matrix(:,26) = (e_vector - (Aux_P_31(:,1).* a_vector + ...
    Aux_P_31(:,2).* b_vector + Aux_P_31(:,3).* c_vector + ...
    Aux_P_31(:,4).* d_vector)) ./ (...
    Aux_Vector_31_14(:,1).* a_vector + ...
    Aux_Vector_31_14(:,2).* b_vector + Aux_Vector_31_14(:,3).* c_vector + ...
    Aux_Vector_31_14(:,4).* d_vector);

lambda_matrix(:,27) = (e_vector - (Aux_P_31(:,1).* a_vector + ...
    Aux_P_31(:,2).* b_vector + Aux_P_31(:,3).* c_vector + ...
    Aux_P_31(:,4).* d_vector)) ./ (...
    Aux_Vector_31_24(:,1).* a_vector + ...
    Aux_Vector_31_24(:,2).* b_vector + Aux_Vector_31_24(:,3).* c_vector + ...
    Aux_Vector_31_24(:,4).* d_vector);

lambda_matrix(:,28) = (e_vector - (Aux_P_31(:,1).* a_vector + ...
    Aux_P_31(:,2).* b_vector + Aux_P_31(:,3).* c_vector + ...
    Aux_P_31(:,4).* d_vector)) ./ (...
    Aux_Vector_31_34(:,1).* a_vector + ...
    Aux_Vector_31_34(:,2).* b_vector + Aux_Vector_31_34(:,3).* c_vector + ...
    Aux_Vector_31_34(:,4).* d_vector);

lambda_matrix(:,29) = (e_vector - (P4_matrix(:,1).* a_vector + ...
    P4_matrix(:,2).* b_vector + P4_matrix(:,3).* c_vector + ...
    P4_matrix(:,4).* d_vector)) ./ (...
    Vector_4_2(:,1).* a_vector + ...
    Vector_4_2(:,2).* b_vector + Vector_4_2(:,3).* c_vector + ...
    Vector_4_2(:,4).* d_vector);

lambda_matrix(:,30) = (e_vector - (P4_matrix(:,1).* a_vector + ...
    P4_matrix(:,2).* b_vector + P4_matrix(:,3).* c_vector + ...
    P4_matrix(:,4).* d_vector)) ./ (...
    Vector_4_3(:,1).* a_vector + ...
    Vector_4_3(:,2).* b_vector + Vector_4_3(:,3).* c_vector + ...
    Vector_4_3(:,4).* d_vector);



Intersection_matrix_1 = P1_matrix + lambda_matrix(:,1).* Vector_1_2;
Intersection_matrix_2 = P2_matrix + lambda_matrix(:,2).* Vector_2_3;
Intersection_matrix_3 = P3_matrix + lambda_matrix(:,3).* Vector_3_1;
Intersection_matrix_4 = P4_matrix + lambda_matrix(:,4).* Vector_4_1;

Intersection_matrix_5 = Aux_P_12 + lambda_matrix(:,5).* Aux_Vector_12_3;
Intersection_matrix_6 = Aux_P_12 + lambda_matrix(:,6).* Aux_Vector_12_4;
Intersection_matrix_7 = Aux_P_23 + lambda_matrix(:,7).* Aux_Vector_23_1;
Intersection_matrix_8 = Aux_P_23 + lambda_matrix(:,8).* Aux_Vector_23_4;
Intersection_matrix_9 = Aux_P_31 + lambda_matrix(:,9).* Aux_Vector_31_2;
Intersection_matrix_10 = Aux_P_31 + lambda_matrix(:,10).* Aux_Vector_31_4;
Intersection_matrix_11 = Aux_P_14 + lambda_matrix(:,11).* Aux_Vector_14_3;
Intersection_matrix_12 = Aux_P_14 + lambda_matrix(:,12).* Aux_Vector_14_2;
Intersection_matrix_13 = Aux_P_24 + lambda_matrix(:,13).* Aux_Vector_24_1;
Intersection_matrix_14 = Aux_P_24 + lambda_matrix(:,14).* Aux_Vector_24_3;
Intersection_matrix_15 = Aux_P_34 + lambda_matrix(:,15).* Aux_Vector_34_1;
Intersection_matrix_16 = Aux_P_34 + lambda_matrix(:,16).* Aux_Vector_34_2;
Intersection_matrix_17 = Aux_P_12 + lambda_matrix(:,17).* Aux_Vector_12_23;
Intersection_matrix_18 = Aux_P_23 + lambda_matrix(:,18).* Aux_Vector_23_31;
Intersection_matrix_19 = Aux_P_31 + lambda_matrix(:,19).* Aux_Vector_31_12;
Intersection_matrix_20 = Aux_P_12 + lambda_matrix(:,20).* Aux_Vector_12_14;
Intersection_matrix_21 = Aux_P_12 + lambda_matrix(:,21).* Aux_Vector_12_24;
Intersection_matrix_22 = Aux_P_12 + lambda_matrix(:,22).* Aux_Vector_12_34;
Intersection_matrix_23 = Aux_P_23 + lambda_matrix(:,23).* Aux_Vector_23_14;
Intersection_matrix_24 = Aux_P_23 + lambda_matrix(:,24).* Aux_Vector_23_24;
Intersection_matrix_25 = Aux_P_23 + lambda_matrix(:,25).* Aux_Vector_23_34;
Intersection_matrix_26 = Aux_P_31 + lambda_matrix(:,26).* Aux_Vector_31_14;
Intersection_matrix_27 = Aux_P_31 + lambda_matrix(:,27).* Aux_Vector_31_24;
Intersection_matrix_28 = Aux_P_31 + lambda_matrix(:,28).* Aux_Vector_31_34;
Intersection_matrix_29 = P4_matrix + lambda_matrix(:,29).* Vector_4_2;
Intersection_matrix_30 = P4_matrix + lambda_matrix(:,30).* Vector_4_3;

% Evaluate if intersection Point is within Delaunay triangle (Interpolation
% can be applied if lambda is between 0 and 1)
Result_index_1 = find(lambda_matrix(:,1) <=1 & lambda_matrix(:,1) >= 0);
Result_index_2 = find(lambda_matrix(:,2) <=1 & lambda_matrix(:,2) >= 0);
Result_index_3 = find(lambda_matrix(:,3) <=1 & lambda_matrix(:,3) >= 0);
Result_index_4 = find(lambda_matrix(:,4) <=1 & lambda_matrix(:,4) >= 0);
Result_index_5 = find(lambda_matrix(:,5) <=1 & lambda_matrix(:,5) >= 0);
Result_index_6 = find(lambda_matrix(:,6) <=1 & lambda_matrix(:,6) >= 0);
Result_index_7 = find(lambda_matrix(:,7) <=1 & lambda_matrix(:,7) >= 0);
Result_index_8 = find(lambda_matrix(:,8) <=1 & lambda_matrix(:,8) >= 0);
Result_index_9 = find(lambda_matrix(:,9) <=1 & lambda_matrix(:,9) >= 0);
Result_index_10 = find(lambda_matrix(:,10) <=1 & lambda_matrix(:,10) >= 0);
Result_index_11 = find(lambda_matrix(:,11) <=1 & lambda_matrix(:,11) >= 0);
Result_index_12 = find(lambda_matrix(:,12) <=1 & lambda_matrix(:,12) >= 0);
Result_index_13 = find(lambda_matrix(:,13) <=1 & lambda_matrix(:,13) >= 0);
Result_index_14 = find(lambda_matrix(:,14) <=1 & lambda_matrix(:,14) >= 0);
Result_index_15 = find(lambda_matrix(:,15) <=1 & lambda_matrix(:,15) >= 0);
Result_index_16 = find(lambda_matrix(:,16) <=1 & lambda_matrix(:,16) >= 0);
Result_index_17 = find(lambda_matrix(:,17) <=1 & lambda_matrix(:,17) >= 0);
Result_index_18 = find(lambda_matrix(:,18) <=1 & lambda_matrix(:,18) >= 0);
Result_index_19 = find(lambda_matrix(:,19) <=1 & lambda_matrix(:,19) >= 0);
Result_index_20 = find(lambda_matrix(:,20) <=1 & lambda_matrix(:,20) >= 0);
Result_index_21 = find(lambda_matrix(:,21) <=1 & lambda_matrix(:,21) >= 0);
Result_index_22 = find(lambda_matrix(:,22) <=1 & lambda_matrix(:,22) >= 0);
Result_index_23 = find(lambda_matrix(:,23) <=1 & lambda_matrix(:,23) >= 0);
Result_index_24 = find(lambda_matrix(:,24) <=1 & lambda_matrix(:,24) >= 0);
Result_index_25 = find(lambda_matrix(:,25) <=1 & lambda_matrix(:,25) >= 0);
Result_index_26 = find(lambda_matrix(:,26) <=1 & lambda_matrix(:,26) >= 0);
Result_index_27 = find(lambda_matrix(:,27) <=1 & lambda_matrix(:,27) >= 0);
Result_index_28 = find(lambda_matrix(:,28) <=1 & lambda_matrix(:,28) >= 0);
Result_index_29 = find(lambda_matrix(:,29) <=1 & lambda_matrix(:,29) >= 0);
Result_index_30 = find(lambda_matrix(:,30) <=1 & lambda_matrix(:,30) >= 0);

% Assign results

Result_vec = Intersection_matrix_1(Result_index_1,:,:);
Result_vec = [Result_vec; Intersection_matrix_2(Result_index_2,:,:)];
Result_vec = [Result_vec; Intersection_matrix_3(Result_index_3,:,:)];
Result_vec = [Result_vec; Intersection_matrix_4(Result_index_4,:,:)];
Result_vec = [Result_vec; Intersection_matrix_5(Result_index_5,:,:)];
Result_vec = [Result_vec; Intersection_matrix_6(Result_index_6,:,:)];
Result_vec = [Result_vec; Intersection_matrix_7(Result_index_7,:,:)];
Result_vec = [Result_vec; Intersection_matrix_8(Result_index_8,:,:)];
Result_vec = [Result_vec; Intersection_matrix_9(Result_index_9,:,:)];
Result_vec = [Result_vec; Intersection_matrix_10(Result_index_10,:,:)];
Result_vec = [Result_vec; Intersection_matrix_11(Result_index_11,:,:)];
Result_vec = [Result_vec; Intersection_matrix_12(Result_index_12,:,:)];
Result_vec = [Result_vec; Intersection_matrix_13(Result_index_13,:,:)];
Result_vec = [Result_vec; Intersection_matrix_14(Result_index_14,:,:)];
Result_vec = [Result_vec; Intersection_matrix_15(Result_index_15,:,:)];
Result_vec = [Result_vec; Intersection_matrix_16(Result_index_16,:,:)];
Result_vec = [Result_vec; Intersection_matrix_17(Result_index_17,:,:)];
Result_vec = [Result_vec; Intersection_matrix_18(Result_index_18,:,:)];
Result_vec = [Result_vec; Intersection_matrix_19(Result_index_19,:,:)];
Result_vec = [Result_vec; Intersection_matrix_20(Result_index_20,:,:)];
Result_vec = [Result_vec; Intersection_matrix_21(Result_index_21,:,:)];
Result_vec = [Result_vec; Intersection_matrix_22(Result_index_22,:,:)];
Result_vec = [Result_vec; Intersection_matrix_23(Result_index_23,:,:)];
Result_vec = [Result_vec; Intersection_matrix_24(Result_index_24,:,:)];
Result_vec = [Result_vec; Intersection_matrix_25(Result_index_25,:,:)];
Result_vec = [Result_vec; Intersection_matrix_26(Result_index_26,:,:)];
Result_vec = [Result_vec; Intersection_matrix_27(Result_index_27,:,:)];
Result_vec = [Result_vec; Intersection_matrix_28(Result_index_28,:,:)];
Result_vec = [Result_vec; Intersection_matrix_29(Result_index_29,:,:)];
Result_vec = [Result_vec; Intersection_matrix_30(Result_index_30,:,:)];


%% Interpolation of additional values
% The interpolation of these values has to be performed but that are not
% subject of the search condition, first thee colums of arg1 are x,y and z
% values, the additional colums are values that should be interpolated for
% the values that fullfill z = arg5

if size(arg1,2) > 4
    for count_interpolants = 5:size(arg1,2)
        
        
        
        P1_matrix = [arg1(T(:,1),1) arg1(T(:,1),2) arg1(T(:,1),3) ...
            arg1(T(:,1),count_interpolants)];
        P2_matrix = [arg1(T(:,2),1) arg1(T(:,2),2) arg1(T(:,2),3) ...
            arg1(T(:,2),count_interpolants)];
        P3_matrix = [arg1(T(:,3),1) arg1(T(:,3),2) arg1(T(:,3),3) ...
            arg1(T(:,3),count_interpolants)];
        P4_matrix = [arg1(T(:,4),1) arg1(T(:,4),2) arg1(T(:,4),3) ...
            arg1(T(:,4),count_interpolants)];
        
        
% Define Points of Hypersimplex
P1_matrix = [arg1(T(:,1),1) arg1(T(:,1),2) arg1(T(:,1),3) arg1(T(:,1),count_interpolants)];
P2_matrix = [arg1(T(:,2),1) arg1(T(:,2),2) arg1(T(:,2),3) arg1(T(:,2),count_interpolants)];
P3_matrix = [arg1(T(:,3),1) arg1(T(:,3),2) arg1(T(:,3),3) arg1(T(:,3),count_interpolants)];
P4_matrix = [arg1(T(:,4),1) arg1(T(:,4),2) arg1(T(:,4),3) arg1(T(:,4),count_interpolants)];

% Define Edges of Hypersimplex

% Hypervector 1: P1 --> P2
Vector_1_2 = P2_matrix - P1_matrix;
% Hypervector 2: P2 --> P3
Vector_2_3 = P3_matrix - P2_matrix;
% Hypervector 3: P3 --> P1
Vector_3_1 = P1_matrix - P3_matrix;
% Hypervector 4: P4 --> P1
Vector_4_1 = P1_matrix - P4_matrix;
% Hypervector 5: P4 --> P2
Vector_4_2 = P2_matrix - P4_matrix;
% Hypervector 6: P4 --> P3
Vector_4_3 = P3_matrix - P4_matrix;


% Aux_P12: Half Vector 1 + P_1
Aux_P_12 = P1_matrix + 0.5 * Vector_1_2;
% Aux_P23: Half Vector 2 + P_2
Aux_P_23 = P2_matrix + 0.5 * Vector_2_3;
% Aux_P31: Half Vector 3 + P_3
Aux_P_31 = P3_matrix + 0.5 * Vector_3_1;
% Aux_P14: Half Vector 4 + P_1
Aux_P_14 = P4_matrix + 0.5 * Vector_4_1;
% Aux_P24: Half Vector 4 + P_2
Aux_P_24 = P4_matrix + 0.5 * Vector_4_1;
% Aux_P34: Half Vector 4 + P_3
Aux_P_34 = P4_matrix + 0.5 * Vector_4_1;


% Define additional hypervectors
Aux_Vector_12_3 = P3_matrix - Aux_P_12;
Aux_Vector_12_4 = P4_matrix - Aux_P_12;
Aux_Vector_23_1 = P1_matrix - Aux_P_23;
Aux_Vector_23_4 = P4_matrix - Aux_P_23;
Aux_Vector_31_2 = P2_matrix - Aux_P_31;
Aux_Vector_31_4 = P4_matrix - Aux_P_31;
Aux_Vector_14_3 = P3_matrix - Aux_P_14;
Aux_Vector_14_2 = P2_matrix - Aux_P_14;
Aux_Vector_24_1 = P1_matrix - Aux_P_24;
Aux_Vector_24_3 = P3_matrix - Aux_P_24;
Aux_Vector_34_1 = P1_matrix - Aux_P_34;
Aux_Vector_34_2 = P2_matrix - Aux_P_34;

Aux_Vector_12_23 =  Aux_P_23 - Aux_P_12;
Aux_Vector_23_31 =  Aux_P_31 - Aux_P_23;
Aux_Vector_31_12 =  Aux_P_12 - Aux_P_31;
Aux_Vector_12_14 =  Aux_P_14 - Aux_P_12;
Aux_Vector_12_24 =  Aux_P_24 - Aux_P_12;
Aux_Vector_12_34 =  Aux_P_34 - Aux_P_12;
Aux_Vector_23_14 =  Aux_P_14 - Aux_P_23;
Aux_Vector_23_24 =  Aux_P_24 - Aux_P_23;
Aux_Vector_23_34 =  Aux_P_34 - Aux_P_23;
Aux_Vector_31_14 =  Aux_P_14 - Aux_P_31;
Aux_Vector_31_24 =  Aux_P_24 - Aux_P_31;
Aux_Vector_31_34 =  Aux_P_34 - Aux_P_31;
        
Intersection_matrix_1 = P1_matrix + lambda_matrix(:,1).* Vector_1_2;
Intersection_matrix_2 = P2_matrix + lambda_matrix(:,2).* Vector_2_3;
Intersection_matrix_3 = P3_matrix + lambda_matrix(:,3).* Vector_3_1;
Intersection_matrix_4 = P4_matrix + lambda_matrix(:,4).* Vector_4_1;

Intersection_matrix_5 = Aux_P_12 + lambda_matrix(:,5).* Aux_Vector_12_3;
Intersection_matrix_6 = Aux_P_12 + lambda_matrix(:,6).* Aux_Vector_12_4;
Intersection_matrix_7 = Aux_P_23 + lambda_matrix(:,7).* Aux_Vector_23_1;
Intersection_matrix_8 = Aux_P_23 + lambda_matrix(:,8).* Aux_Vector_23_4;
Intersection_matrix_9 = Aux_P_31 + lambda_matrix(:,9).* Aux_Vector_31_2;
Intersection_matrix_10 = Aux_P_31 + lambda_matrix(:,10).* Aux_Vector_31_4;
Intersection_matrix_11 = Aux_P_14 + lambda_matrix(:,11).* Aux_Vector_14_3;
Intersection_matrix_12 = Aux_P_14 + lambda_matrix(:,12).* Aux_Vector_14_2;
Intersection_matrix_13 = Aux_P_24 + lambda_matrix(:,13).* Aux_Vector_24_1;
Intersection_matrix_14 = Aux_P_24 + lambda_matrix(:,14).* Aux_Vector_24_3;
Intersection_matrix_15 = Aux_P_34 + lambda_matrix(:,15).* Aux_Vector_34_1;
Intersection_matrix_16 = Aux_P_34 + lambda_matrix(:,16).* Aux_Vector_34_2;
Intersection_matrix_17 = Aux_P_12 + lambda_matrix(:,17).* Aux_Vector_12_23;
Intersection_matrix_18 = Aux_P_23 + lambda_matrix(:,18).* Aux_Vector_23_31;
Intersection_matrix_19 = Aux_P_31 + lambda_matrix(:,19).* Aux_Vector_31_12;
Intersection_matrix_20 = Aux_P_12 + lambda_matrix(:,20).* Aux_Vector_12_14;
Intersection_matrix_21 = Aux_P_12 + lambda_matrix(:,21).* Aux_Vector_12_24;
Intersection_matrix_22 = Aux_P_12 + lambda_matrix(:,22).* Aux_Vector_12_34;
Intersection_matrix_23 = Aux_P_23 + lambda_matrix(:,23).* Aux_Vector_23_14;
Intersection_matrix_24 = Aux_P_23 + lambda_matrix(:,24).* Aux_Vector_23_24;
Intersection_matrix_25 = Aux_P_23 + lambda_matrix(:,25).* Aux_Vector_23_34;
Intersection_matrix_26 = Aux_P_31 + lambda_matrix(:,26).* Aux_Vector_31_14;
Intersection_matrix_27 = Aux_P_31 + lambda_matrix(:,27).* Aux_Vector_31_24;
Intersection_matrix_28 = Aux_P_31 + lambda_matrix(:,28).* Aux_Vector_31_34;
Intersection_matrix_29 = P4_matrix + lambda_matrix(:,29).* Vector_4_2;
Intersection_matrix_30 = P4_matrix + lambda_matrix(:,30).* Vector_4_3;

% Get results        
Temp_result_vec = Intersection_matrix_1(Result_index_1,4,:);
Temp_result_vec = [Temp_result_vec; Intersection_matrix_2(Result_index_2,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_3(Result_index_3,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_4(Result_index_4,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_5(Result_index_5,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_6(Result_index_6,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_7(Result_index_7,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_8(Result_index_8,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_9(Result_index_9,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_10(Result_index_10,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_11(Result_index_11,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_12(Result_index_12,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_13(Result_index_13,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_14(Result_index_14,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_15(Result_index_15,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_16(Result_index_16,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_17(Result_index_17,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_18(Result_index_18,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_19(Result_index_19,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_20(Result_index_20,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_21(Result_index_21,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_22(Result_index_22,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_23(Result_index_23,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_24(Result_index_24,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_25(Result_index_25,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_26(Result_index_26,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_27(Result_index_27,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_28(Result_index_28,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_29(Result_index_29,4,:)];
Temp_result_vec = [Temp_result_vec; Intersection_matrix_30(Result_index_30,4,:)];
% Assign Results to Ouput vector
Result_vec = [Result_vec Temp_result_vec];
        
    end
end

Result_vec = unique(Result_vec,'Rows');



