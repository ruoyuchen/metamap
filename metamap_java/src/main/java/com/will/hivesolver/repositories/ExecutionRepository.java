package com.will.hivesolver.repositories;

import com.will.hivesolver.entity.Execution;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * Created by will on 16-7-13.
 */
public interface ExecutionRepository extends JpaRepository<Execution, Integer>{
}