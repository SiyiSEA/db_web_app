# All these codes are for parse the data for the hackthon db
library(data.table)


main <- function() 
{
    # Args
    arguments <- commandArgs(T)
    work_path <- arguments[1]
    db_path <- arguments[2]
    pheno_file <- arguments[3]
    epic_file <- arguments[4]
    betas <- arguments[5]

    # set the directory
    setwd(work_path)

    # load the data #########################################################
    message('Loading data........................')
    pheno <-  fread(pheno_file, data.table = F) 
    epic <-  fread(epic_file, data.table = F) 
    beta <-  fread(betas, data.table = F) 

    # Pheno.csv for creating PHENO table ###############################
    message('Creating PHENO table........................')
    # Step1 - rename the colname for pheno
    sex_index = grep("^Sex$", names(pheno), ignore.case = TRUE)
    if (length(sex_index) != 0) {colnames(pheno)[sex_index] <- 'Sex'}
    age_index = grep("^PCW$", names(pheno), ignore.case = TRUE)
    if (length(age_index) != 0) {colnames(pheno)[age_index] <- 'Age'}
    SID_index = grep("^Sample_ID$", names(pheno), ignore.case = TRUE)
    if (length(SID_idnex) != 0) {colnames(pheno)[SID_index] <- 'SID'}
    IID_index = grep("^Individual_ID$", names(pheno), ignore.case = TRUE)
    if (length(IID_idnex) != 0) {colnames(pheno)[IID_index] <- 'IID'}
    colnames(pheno)[1] <- 'SampleName'
    pheno$SampleKey <- 1:nrow(pheno)
 
    sample_info <- data.frame(SampleName = colnames(beta)[2:ncol(beta)],
                          SampleKey = 1:(ncol(beta)-1))
    pheno <-merge(sample_info, pheno, by.x = 'SampleName', by.y = 'SampleName')

    # Step2 - pick the necessary columns 
    sample_info <- pheno[,c('SampleName', 'SampleKey')]
    pheno <- pheno[,c('SampleKey', 'Age', 'Sex')]
    write.csv(pheno, paste0('./',db_path,'/Siyi_pheno.csv'), row.names = F)

    # Epic.csv for creating EPIC table ################################
    message('Creating PORBEINFO and EPIC table........................')
    # Step1 - sort the table and add ProbeKey
    m <- match(beta[,'V1'], epic[,'Name'])
    epic <- epic[m,]

    # Step2 - PORBEINFO table
    probe_info <- data.frame(ProbeName = beta$V1,
                            ProbeKey = 1:length(beta$V1))
    write.csv(probe_info, paste0('./', db_path,'Siyi_Probe_info_more.csv'), row.names = F)

    # Step3 - EPIC
    epic <- epic[, c('Name', 'CHR','Gene', 'Group', 'Island')]
    epic <- merge(epic, probe_info, by.x = 'Name', by.y = 'ProbeName')
    epic <- epic[,c('ProbeKey', 'CHR', 'Gene', 'Group', 'Island')]
    write.csv(epic, paste0('./', db_path, '/Siyi_epic.csv'), row.names = F) 

    # Betas.csv #############################################
    message('Creating several beta tables........................')
    # Step1 - replace CpG(V1) by ProbeKey
    if (length(unique(beta$V1)) == nrow(beta)) {
    message('There is no duplication CpG data, continuing...')
    beta <- merge(beta, probe_info, by.x = 'V1', by.y = 'ProbeName')
    row.names(beta) <- beta[,which(colnames(beta)=='ProbeKey')]
    beta <- beta[,-1]
    }else{
    stop('There are duplication CpGs in beta matrix, Stop!')
    }

    # Setp2 - replace SampleName(column name) by SampleKey
    new_row <- list(SampleName = 'ProbeKey', SampleKey = 'ProbeKey')
    sample_info <- rbind(sample_info, new_row)
    sample_info_t <- as.data.frame(t(sample_info))
    colnames(sample_info_t) <- sample_info_t['SampleName',]
    sample_info_t <- sample_info_t[-1,]

    # make sure the column name of sample_info_t and the be_cp are identical
    if (length(colnames(sample_info_t)) == length(colnames(beta))) {
    beta <- rbind(beta, sample_info_t)
    colnames(beta) <- beta[which(rownames(beta) == 'SampleKey'),]
    beta <- beta[-which(rownames(beta) == 'SampleKey'),]
    }else{
    stop("The number of sample from phen is not match with the sample from beta. Stop!")
    }

    # Setp3 - split the beta into 4 tables
    gap <-  round((nrow(beta)-1) / 4)

    be_A <- beta[1:gap,]
    be_B <- beta[gap + 1 :gap * 2,]
    be_C <- beta[gap * 2 + 1:gap * 3,]
    be_D <- beta[gap * 3 + 1:(nrow(beta)-1),]

    # melt the beta ABCD tbale
    library(reshape2)
    be_A_melt <- melt(be_A, id = c('ProbeKey'))
    be_B_melt <- melt(be_B, id = c('ProbeKey'))
    be_C_melt <- melt(be_C, id = c('ProbeKey'))
    be_D_melt <- melt(be_D, id = c('ProbeKey'))

    # rename the tables
    colnames(be_A_melt) = c('ProbeKey', 'SampleKey', 'Value')
    colnames(be_B_melt) = c('ProbeKey', 'SampleKey', 'Value')
    colnames(be_C_melt) = c('ProbeKey', 'SampleKey', 'Value')
    colnames(be_D_melt) = c('ProbeKey', 'SampleKey', 'Value')

    # save the tables
    write.csv(be_A_melt, paste0('./', db_path, '/Siyi_A_betas.csv'), row.names = F)
    write.csv(be_B_melt, paste0('./', db_path, '/Siyi_B_betas.csv'), row.names = F)
    write.csv(be_C_melt, paste0('./', db_path, '/Siyi_C_betas.csv'), row.names = F)
    write.csv(be_D_melt, paste0('./', db_path, '/Siyi_D_betas.csv'), row.names = F)

    message('All the files are ready for the building the database, done!')
}

