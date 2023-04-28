%chk=CO_15_0_15_15_90.chk
%mem=20GB
%nprocshared=16
# opt B3LYP/6-31g(d,p) scrf=iefpcm

job_CO_15_0_15_15_90

0 1
    C           0       1.177  -3.324   8.204
    C           0       1.892  -2.256   7.628
    C           0       1.588  -1.866   6.307
    C           0       0.609  -2.538   5.585
    C           0      -0.113  -3.588   6.190
    C           0       0.174  -3.985   7.499
    H           0       1.385  -3.615   9.229
    H           0       2.139  -1.046   5.860
    H           0      -0.383  -4.789   7.972
    C           0       0.106  -2.277   4.158
    C           0      -1.001  -3.336   4.046
    C           0      -1.815  -3.646   2.963
    C           0      -2.776  -4.673   3.065
    C           0      -2.885  -5.384   4.276
    C           0      -2.056  -5.099   5.359
    C           0      -1.110  -4.079   5.241
    H           0      -1.732  -3.093   2.034
    H           0      -3.605  -6.193   4.357
    H           0      -2.141  -5.678   6.274
    C           0      -3.651  -5.007   1.914
    C           0      -3.356  -4.549   0.617
    C           0      -4.800  -5.800   2.078
    C           0      -4.172  -4.867  -0.462
    H           0      -2.465  -3.953   0.446
    C           0      -5.621  -6.123   1.001
    H           0      -5.065  -6.162   3.066
    C           0      -5.325  -5.657  -0.290
    H           0      -3.921  -4.517  -1.457
    H           0      -6.487  -6.749   1.173
    C           0      -6.108  -5.999  -1.490
    C           0      -7.758  -6.658  -2.845
    C           0      -6.633  -6.257  -3.557
    C           0      -8.968  -7.096  -3.491
    C           0      -6.584  -6.302  -4.991
    C           0      -8.942  -7.149  -4.927
    C           0      -7.743  -6.760  -5.681
    C           0     -10.155  -7.453  -2.810
    C           0     -11.282  -7.866  -3.498
    C           0     -10.115  -7.579  -5.588
    C           0     -11.262  -7.934  -4.898
    C           0      -5.431  -5.912  -5.705
    C           0      -7.676  -6.812  -7.094
    C           0      -5.404  -5.973  -7.086
    C           0      -6.537  -6.428  -7.783
    N           0      -7.408  -6.497  -1.503
    N           0      -5.630  -5.851  -2.715
    C           0      -8.249  -6.692  -0.354
    C           0      -8.223  -7.912   0.328
    C           0      -9.082  -5.655   0.071
    C           0      -9.042  -8.093   1.442
    H           0      -7.569  -8.706  -0.017
    C           0      -9.895  -5.842   1.190
    H           0      -9.091  -4.716  -0.472
    C           0      -9.877  -7.060   1.875
    H           0      -9.025  -9.040   1.973
    H           0     -10.543  -5.037   1.524
    H           0     -10.512  -7.203   2.743
    H           0     -12.181  -8.134  -2.949
    H           0     -12.142  -8.257  -5.444
    H           0     -10.132  -7.632  -6.670
    H           0     -10.189  -7.401  -1.730
    H           0      -8.528  -7.158  -7.668
    H           0      -6.523  -6.482  -8.867
    H           0      -4.513  -5.673  -7.630
    H           0      -4.568  -5.567  -5.144
    C           0      -0.445  -0.817   4.096
    H           0       0.368  -0.144   4.393
    H           0      -1.212  -0.719   4.875
    C           0       1.183  -2.569   3.066
    H           0       1.536  -3.598   3.212
    H           0       0.678  -2.563   2.092
    C           0       2.394  -1.630   2.988
    H           0       2.978  -1.690   3.914
    H           0       2.062  -0.588   2.896
    C           0       3.312  -1.962   1.802
    H           0       3.672  -2.996   1.898
    H           0       2.728  -1.928   0.871
    C           0       4.510  -1.013   1.681
    H           0       5.096  -1.045   2.610
    H          -1       4.143   0.019   1.588
    C          -1       5.426  -1.331   0.492
    H          -1       5.819  -2.352   0.596
    H          -1       4.834  -1.325  -0.434
    C          -1       6.595  -0.349   0.346
    H          -1       7.188  -0.349   1.272
    H          -1       6.199   0.671   0.238
    C          -1       7.508  -0.668  -0.843
    H          -1       6.921  -0.679  -1.771
    H          -1       7.934  -1.672  -0.729
    C          -1       8.652   0.345  -0.992
    H          -1       9.261   0.368  -0.083
    C          -1      10.660  -0.751  -2.085
    C          -1       9.341   0.487  -3.427
    C          -1      11.253  -1.422  -1.011
    C          -1      11.214  -0.842  -3.388
    C          -1       8.347   1.309  -3.970
    C          -1      10.365  -0.046  -4.251
    C          -1      12.400  -2.169  -1.261
    H          -1      10.840  -1.372  -0.009
    C          -1      12.371  -1.603  -3.606
    C          -1       8.401   1.586  -5.332
    H          -1       7.550   1.720  -3.358
    C          -1      10.390   0.254  -5.621
    C          -1      12.984  -2.280  -2.548
    H          -1      12.859  -2.687  -0.425
    H          -1      12.780  -1.659  -4.608
    C          -1       9.410   1.074  -6.185
    H          -1       7.627   2.224  -5.749
    H          -1      11.182  -0.163  -6.233
    N          -1       9.536   0.067  -2.117
    C          -1      -1.022  -0.322   2.763
    H          -1      -1.909  -0.909   2.496
    H          -1      -0.296  -0.467   1.954
    C          -1      -1.409   1.163   2.823
    H          -1      -0.522   1.756   3.089
    H          -1      -2.133   1.319   3.635
    C          -1      -1.995   1.696   1.510
    H          -1      -1.279   1.520   0.695
    H          -1      -2.896   1.121   1.253
    C          -1      -2.343   3.189   1.561
    H          -1      -1.441   3.761   1.821
    H          -1      -3.062   3.368   2.373
    C          -1      -2.919   3.728   0.246
    H          -1      -2.207   3.532  -0.568
    H          -1      -3.833   3.173  -0.006
    C          -1      -3.230   5.229   0.294
    H          -1      -2.319   5.789   0.540
    H          -1      -3.951   5.436   1.094
    C          -1      -3.793   5.752  -1.035
    H          -1      -3.090   5.550  -1.850
    C          -1      -5.261   7.781  -0.631
    C          -1      -3.159   8.188  -1.331
    C          -1      -6.464   7.199  -0.216
    C          -1      -5.126   9.191  -0.700
    C          -1      -1.830   8.095  -1.757
    C          -1      -3.775   9.453  -1.151
    C          -1      -7.516   8.046   0.121
    H          -1      -6.584   6.123  -0.149
    C          -1      -6.207  10.015  -0.355
    C          -1      -1.141   9.279  -2.001
    H          -1      -1.339   7.137  -1.890
    C          -1      -3.051  10.626  -1.409
    C          -1      -7.419   9.459   0.062
    H          -1      -8.447   7.592   0.445
    H          -1      -6.084  11.091  -0.415
    C          -1      -1.723  10.560  -1.838
    H          -1      -0.108   9.205  -2.329
    H          -1      -3.540  11.584  -1.267
    N          -1      -4.071   7.183  -1.030
    H          -1      -4.720   5.229  -1.288
    H          -1       8.250   1.356  -1.122
    C          -1      -8.636  10.317   0.462
    C          -1      -9.011  10.027   1.935
    H          -1      -8.181  10.277   2.605
    H          -1      -9.879  10.626   2.233
    H          -1      -9.263   8.974   2.092
    C          -1      -9.839   9.970  -0.447
    H          -1      -9.608  10.176  -1.497
    H          -1     -10.121   8.916  -0.366
    H          -1     -10.713  10.569  -0.167
    C          -1      -8.356  11.825   0.328
    H          -1      -7.533  12.146   0.975
    H          -1      -8.109  12.105  -0.702
    H          -1      -9.246  12.392   0.620
    C          -1      -0.878  11.817  -2.127
    C          -1      -0.381  11.786  -3.592
    H          -1       0.236  10.906  -3.796
    H          -1      -1.224  11.773  -4.291
    H          -1       0.225  12.674  -3.807
    C          -1       0.343  11.848  -1.178
    H          -1       0.960  12.732  -1.378
    H          -1       0.023  11.888  -0.131
    H          -1       0.977  10.965  -1.302
    C          -1      -1.677  13.118  -1.922
    H          -1      -2.545  13.172  -2.588
    H          -1      -2.031  13.220  -0.891
    H          -1      -1.038  13.980  -2.139
    C          -1       9.390   1.438  -7.683
    C          -1      10.550   0.785  -8.457
    H          -1      10.510  -0.308  -8.407
    H          -1      10.494   1.070  -9.513
    H          -1      11.525   1.109  -8.079
    C          -1       9.507   2.972  -7.844
    H          -1       8.688   3.498  -7.345
    H          -1      10.448   3.338  -7.420
    H          -1       9.483   3.248  -8.905
    C          -1       8.062   0.960  -8.317
    H          -1       7.193   1.421  -7.838
    H          -1       8.032   1.218  -9.381
    H          -1       7.956  -0.127  -8.229
    C          -1      14.257  -3.130  -2.729
    C          -1      15.393  -2.558  -1.847
    H          -1      15.630  -1.528  -2.135
    H          -1      15.124  -2.557  -0.787
    H          -1      16.303  -3.159  -1.959
    C          -1      14.747  -3.141  -4.190
    H          -1      15.651  -3.754  -4.269
    H          -1      13.999  -3.566  -4.867
    H          -1      14.997  -2.136  -4.544
    C          -1      13.973  -4.591  -2.308
    H          -1      13.660  -4.660  -1.261
    H          -1      13.180  -5.028  -2.924
    H           0      14.873  -5.204  -2.428
    C           0       2.942  -1.547   8.400
    C           0       3.436  -0.297   7.975
    C           0       3.475  -2.100   9.579
    C           0       4.418   0.366   8.698
    H           0       3.026   0.167   7.084
    C           0       4.457  -1.434  10.305
    H           0       3.133  -3.072   9.917
    C           0       4.945  -0.190   9.876
    H           0       4.788   1.332   8.371
    H           0       4.847  -1.897  11.205
    C           0       6.000   0.566  10.617
    O           0       6.397   1.652  10.203
    C           0       6.573  -0.028  11.889
    H           0       5.788  -0.186  12.635
    H           0       7.036  -1.002  11.692
    H           0       7.323   0.653  12.292

